#!/usr/bin/env node

const fs = require("fs/promises");
const path = require("path");
const os = require("os");
const { spawn, spawnSync } = require("child_process");
const dotenv = require("dotenv");

const ROOT = path.resolve(__dirname, "..", "..", "..");
dotenv.config({ path: path.join(ROOT, ".env") });

const TEMPLATE_PATH = path.join(
    ROOT,
    "./.github/scripts/figma-export/figma-export-icons.template.json"
);
const ICONS_ROOT = path.join(ROOT, "icons");
const README_GENERATOR_PATH = path.join(
    ROOT,
    ".github/scripts/md-generator/generate_markdown.py"
);
const { BRANDS } = require("./brands.config");

(async () => {
    try {
        const options = parseArgs(process.argv.slice(2));

        if (options.help) {
            printHelp();
            return;
        }

        const brands = resolveBrandSelection(options.brand);
        const token = options.token || process.env.FIGMA_TOKEN;

        if (!options.skipExport && !token) {
            throw new Error(
                "Missing FIGMA_TOKEN. Pass --token <value> or export FIGMA_TOKEN in your shell."
            );
        }

        let template = null;
        if (!options.skipExport) {
            template = await loadTemplate();
        }
        const generatedConfigFiles = new Set();

        console.log(
            `Exporting brands: ${brands
                .map((key) => BRANDS[key].label)
                .join(", ")}`
        );

        try {
            if (!options.skipExport) {
                for (const brandKey of brands) {
                    const ready = await prepareConfigsForBrand(
                        brandKey,
                        token,
                        template,
                        generatedConfigFiles
                    );

                    if (!ready) continue;

                    await runExportsForBrand(brandKey);
                }
            } else {
                console.log("Skipping Figma export step");
            }

            if (!options.skipSvgo) {
                const svgoTargets =
                    options.brand === "all"
                        ? ["icons"]
                        : dedupe(
                              brands.flatMap((key) => BRANDS[key].svgoTargets)
                          );
                await optimizeWithSvgo(svgoTargets);
            } else {
                console.log("Skipping SVGO optimization");
            }

            if (!options.skipPdf) {
                const toolStatus = await ensureCliTools();
                const pdfTargets =
                    options.brand === "all"
                        ? [ICONS_ROOT]
                        : dedupe(
                              brands.flatMap((key) =>
                                  BRANDS[key].variants.map((variant) =>
                                      path.join(ROOT, variant.iconsPath)
                                  )
                              )
                          );
                await convertSvgToPdf(pdfTargets, Boolean(toolStatus.hasQpdf));
            } else {
                console.log("Skipping PDF conversion");
            }

            if (!options.skipReadme) {
                await runReadmeGenerator();
            } else {
                console.log("Skipping README generation");
            }

            console.log("Done!");
        } finally {
            await cleanupConfigs(generatedConfigFiles);
        }
    } catch (error) {
        console.error(`\nError: ${error.message}`);
        process.exitCode = 1;
    }
})();

function parseArgs(argv) {
    const options = {
        brand: "all",
        skipExport: false,
        skipSvgo: false,
        skipPdf: false,
        skipReadme: false,
        help: false,
        token: undefined,
    };

    for (let i = 0; i < argv.length; i += 1) {
        const arg = argv[i];

        if (arg === "--help" || arg === "-h") {
            options.help = true;
            continue;
        }

        if (arg.startsWith("--brand")) {
            const { value, offset } = readOptionValue(arg, argv, i);
            options.brand = value.trim();
            i += offset;
            continue;
        }

        if (arg.startsWith("--token")) {
            const { value, offset } = readOptionValue(arg, argv, i);
            options.token = value.trim();
            i += offset;
            continue;
        }

        if (arg === "--skip-export") {
            options.skipExport = true;
            continue;
        }

        if (arg === "--skip-svgo") {
            options.skipSvgo = true;
            continue;
        }

        if (arg === "--skip-pdf") {
            options.skipPdf = true;
            continue;
        }

        if (arg === "--skip-readme") {
            options.skipReadme = true;
            continue;
        }

        throw new Error(
            `Unknown argument: ${arg}. Use --help to see the available options.`
        );
    }

    return options;
}

function readOptionValue(arg, argv, index) {
    const eqIndex = arg.indexOf("=");
    if (eqIndex !== -1) {
        const value = arg.slice(eqIndex + 1);
        if (value) {
            return { value, offset: 0 };
        }
        throw new Error(`Missing value for ${arg}`);
    }

    const nextValue = argv[index + 1];
    if (!nextValue) {
        throw new Error(`Missing value for ${arg}`);
    }

    return { value: nextValue, offset: 1 };
}

function printHelp() {
    console.log(`Usage: npm run figma-export -- [options]

Options:
  --brand <name[,name,...]>   Brand(s) to export (${Object.keys(BRANDS).join(", ")}, or "all")
    --skip-export              Skip downloading from Figma (post-process only)
  --token <value>             Figma personal token (or set FIGMA_TOKEN)
  --skip-svgo                 Skip SVG optimization
  --skip-pdf                  Skip PDF generation
  --skip-readme               Skip markdown regeneration
  -h, --help                  Display this help message

Examples:
  yarn figma-export -- --brand telefonica
  yarn run figma-export -- --brand telefonica,o2
  FIGMA_TOKEN=xxx yarn figma-export -- --brand all
`);
}

function resolveBrandSelection(value) {
    if (!value || value.toLowerCase() === "all") {
        return Object.keys(BRANDS);
    }

    const requested = value
        .split(",")
        .map((entry) => entry.trim().toLowerCase())
        .filter(Boolean);

    if (!requested.length) {
        throw new Error("Please specify at least one brand after --brand.");
    }

    const unique = dedupe(requested);
    const invalid = unique.filter((key) => !BRANDS[key]);

    if (invalid.length) {
        throw new Error(`Unknown brand(s): ${invalid.join(", ")}`);
    }

    return Object.keys(BRANDS).filter((brand) => unique.includes(brand));
}

function dedupe(items) {
    return [...new Set(items)];
}

async function loadTemplate() {
    try {
        const raw = await fs.readFile(TEMPLATE_PATH, "utf8");
        const template = JSON.parse(raw);
        if (!template.page) {
            template.page = "Icons";
        }
        return template;
    } catch (error) {
        if (error.code === "ENOENT") {
            throw new Error("Missing figma-export-icons.template.json");
        }
        throw error;
    }
}

async function prepareConfigsForBrand(
    brandKey,
    token,
    template,
    generatedFiles
) {
    const brand = BRANDS[brandKey];

    if (!brand) {
        throw new Error(`Unsupported brand: ${brandKey}`);
    }

    const fileId = process.env[brand.figmaEnv] || brand.defaultFileId;

    if (!fileId) {
        console.log(`\nSkipping ${brand.label}: no Figma file ID configured`);
        return false;
    }

    console.log(`\nSetting up configs for ${brand.label}`);

    for (const variant of brand.variants) {
        const configPayload = {
            ...template,
            figmaPersonalToken: token,
            fileId,
            frame: variant.frame,
            iconsPath: variant.iconsPath,
        };

        const destination = path.join(ROOT, variant.configName);
        await fs.writeFile(
            destination,
            JSON.stringify(configPayload, null, 2) + "\n"
        );
        generatedFiles.add(destination);
    }

    return true;
}

async function runExportsForBrand(brandKey) {
    const brand = BRANDS[brandKey];

    console.log(`Exporting ${brand.label} icons`);

    for (const variant of brand.variants) {
        await runCommand("npm", ["run", variant.script]);
    }
}

async function optimizeWithSvgo(targets) {
    if (!targets.length) {
        return;
    }

    console.log("\nOptimizing SVGs with SVGO");

    for (const target of targets) {
        await fs.mkdir(path.resolve(ROOT, target), { recursive: true });
        await runCommand("npx", ["svgo", "-f", target, "-r", "-o", target]);
    }
}

async function ensureCliTools() {
    const checks = [
        {
            command: "rsvg-convert",
            hint: "brew install librsvg",
            required: true,
        },
        { command: "exiftool", hint: "brew install exiftool", required: true },
        { command: "qpdf", hint: "brew install qpdf", required: false },
    ];

    const status = {};

    for (const check of checks) {
        const exists = commandExists(check.command);

        if (!exists && check.required) {
            throw new Error(
                `${check.command} not found. Install it first (e.g. ${check.hint}).`
            );
        }

        if (!exists) {
            console.warn(
                `Warning: ${check.command} not found. (${check.hint})`
            );
        }

        status[`has${capitalize(check.command)}`] = exists;
    }

    return { hasQpdf: status.hasQpdf || false };
}

function commandExists(command) {
    const result = spawnSync("which", [command], { stdio: "ignore" });
    return result.status === 0;
}

async function convertSvgToPdf(sourceDirs, hasQpdf) {
    console.log("\nConverting SVGs to PDF");

    const svgFiles = [];

    for (const dir of sourceDirs) {
        if (!(await directoryExists(dir))) {
            continue;
        }
        const files = await collectSvgFiles(dir);
        svgFiles.push(...files);
    }

    if (!svgFiles.length) {
        console.log("No SVG files found for the selected brand(s).");
        return;
    }

    let updatedCount = 0;
    let processedCount = 0;
    const total = svgFiles.length;
    const progressMode = process.stdout.isTTY
        ? "interactive"
        : process.env.CI
        ? "ci"
        : "off";
    const progressEnabled = progressMode !== "off" && total > 1;
    let progressActive = false;
    let lastPercentLogged = -1;

    const clearProgress = () => {
        if (progressMode !== "interactive" || !progressActive) {
            return;
        }
        process.stdout.write("\r\x1B[K");
        progressActive = false;
    };

    const renderProgress = (forceLog = false) => {
        if (!progressEnabled) {
            return;
        }
        const percent = Math.floor((processedCount / total) * 100);
        const width = 30;
        const filled = Math.round((percent / 100) * width);
        const bar = "#".repeat(filled).padEnd(width, "-");
        if (progressMode === "interactive") {
            process.stdout.write(
                `\r[${bar}] ${percent}% (${processedCount}/${total})`
            );
            progressActive = true;
            return;
        }

        if (percent !== lastPercentLogged || forceLog) {
            console.log(`[${bar}] ${percent}% (${processedCount}/${total})`);
            lastPercentLogged = percent;
        }
    };

    const logWithProgress = (message) => {
        if (progressMode === "interactive") {
            clearProgress();
            console.log(message);
            renderProgress(true);
            return;
        }

        console.log(message);
    };

    if (progressEnabled) {
        renderProgress(true);
    }

    for (const svgPath of svgFiles) {
        const tmpDir = await fs.mkdtemp(
            path.join(os.tmpdir(), "mistica-icons-")
        );
        const tmpPdf = path.join(tmpDir, "icon.pdf");

        await runCommand("rsvg-convert", ["-f", "pdf", "-o", tmpPdf, svgPath], {
            env: { ...process.env, SOURCE_DATE_EPOCH: "0" },
        });

        await runCommand(
            "exiftool",
            ["-all:all=", "-overwrite_original", tmpPdf],
            {
                stdio: "ignore",
            }
        );

        if (hasQpdf) {
            await runCommand(
                "qpdf",
                [
                    "--replace-input",
                    "--deterministic-id",
                    "--object-streams=preserve",
                    "--stream-data=preserve",
                    tmpPdf,
                ],
                { stdio: "ignore", allowFailure: true }
            );
        }

        await fs.utimes(tmpPdf, 0, 0);

        const targetPdf = svgPath.replace(/\.svg$/i, ".pdf");
        const changed = await maybeReplaceFile(tmpPdf, targetPdf);

        if (changed) {
            updatedCount += 1;
            logWithProgress(`Updated ${path.relative(ROOT, targetPdf)}`);
        }

        await fs.rm(tmpDir, { recursive: true, force: true });

        processedCount += 1;
        renderProgress();
    }

    if (progressMode === "interactive" && progressActive) {
        clearProgress();
        process.stdout.write("\n");
    }

    if (!updatedCount) {
        console.log("No PDF changes detected.");
    }
}

async function collectSvgFiles(dir, acc = []) {
    const entries = await fs.readdir(dir, { withFileTypes: true });

    for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
            await collectSvgFiles(fullPath, acc);
            continue;
        }

        if (entry.isFile() && entry.name.toLowerCase().endsWith(".svg")) {
            acc.push(fullPath);
        }
    }

    return acc;
}

async function maybeReplaceFile(source, target) {
    await fs.mkdir(path.dirname(target), { recursive: true });

    if (await filesAreEqual(source, target)) {
        return false;
    }

    // copy instead of rename so we work across filesystems (/tmp vs repo path)
    await fs.copyFile(source, target);
    return true;
}

async function filesAreEqual(source, target) {
    if (!(await fileExists(target))) {
        return false;
    }

    const [existing, incoming] = await Promise.all([
        fs.readFile(target),
        fs.readFile(source),
    ]);

    return existing.equals(incoming);
}

async function fileExists(filePath) {
    try {
        await fs.access(filePath);
        return true;
    } catch (error) {
        if (error.code === "ENOENT") {
            return false;
        }
        throw error;
    }
}

async function directoryExists(dirPath) {
    try {
        const stats = await fs.stat(dirPath);
        return stats.isDirectory();
    } catch (error) {
        if (error.code === "ENOENT") {
            return false;
        }
        throw error;
    }
}

async function cleanupConfigs(files) {
    await Promise.all(
        [...files].map(async (filePath) => {
            try {
                await fs.unlink(filePath);
            } catch (error) {
                if (error.code !== "ENOENT") {
                    throw error;
                }
            }
        })
    );
}

async function runReadmeGenerator() {
    if (!(await fileExists(README_GENERATOR_PATH))) {
        console.warn(
            "README generator script not found; skipping markdown update."
        );
        return;
    }

    console.log("\nRe-generating markdown catalog");
    await runCommand("python3", [README_GENERATOR_PATH, "icons"]);
}

function runCommand(command, args, options = {}) {
    const {
        cwd = ROOT,
        stdio = "inherit",
        env = process.env,
        allowFailure = false,
    } = options;

    return new Promise((resolve, reject) => {
        const child = spawn(command, args, { cwd, stdio, env });

        child.on("close", (code) => {
            if (code === 0 || (allowFailure && code !== 0)) {
                resolve(code);
            } else {
                reject(
                    new Error(`Command failed: ${command} ${args.join(" ")}`)
                );
            }
        });
    });
}

function capitalize(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
}
