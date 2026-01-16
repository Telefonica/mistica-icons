#!/usr/bin/env node

const fs = require("fs/promises");
const path = require("path");
const os = require("os");
const { spawn, spawnSync } = require("child_process");
const dotenv = require("dotenv");

const ROOT = path.resolve(__dirname, "..", "..");
dotenv.config({ path: path.join(ROOT, ".env") });

const TEMPLATE_PATH = path.join(ROOT, "figma-export-icons.template.json");
const ICONS_ROOT = path.join(ROOT, "icons");
const BRAND_ORDER = ["telefonica", "o2", "o2-new", "blau", "vivo"];

const BRANDS = {
    telefonica: {
        label: "Telefonica",
        figmaEnv: "TELEFONICA_FIGMA_ID",
        defaultFileId: "JXy7Y07eb0Axg0ThVRWKju",
        svgoTargets: ["icons/telefonica"],
        variants: [
            {
                configName: "telefonica-filled.json",
                frame: "Filled",
                iconsPath: "icons/telefonica/filled",
                script: "export-telefonica-filled",
            },
            {
                configName: "telefonica-regular.json",
                frame: "Regular",
                iconsPath: "icons/telefonica/regular",
                script: "export-telefonica-regular",
            },
            {
                configName: "telefonica-light.json",
                frame: "Light",
                iconsPath: "icons/telefonica/light",
                script: "export-telefonica-light",
            },
        ],
    },
    o2: {
        label: "O2",
        figmaEnv: "O2_FIGMA_ID",
        defaultFileId: "wHTqJ7KDhGKrNSNpmMb9nW",
        svgoTargets: ["icons/o2"],
        variants: [
            {
                configName: "o2-filled.json",
                frame: "Filled",
                iconsPath: "icons/o2/filled",
                script: "export-o2-filled",
            },
            {
                configName: "o2-regular.json",
                frame: "Regular",
                iconsPath: "icons/o2/regular",
                script: "export-o2-regular",
            },
            {
                configName: "o2-light.json",
                frame: "Light",
                iconsPath: "icons/o2/light",
                script: "export-o2-light",
            },
        ],
    },
    "o2-new": {
        label: "O2-new",
        figmaEnv: "O2_NEW_FIGMA_ID",
        defaultFileId: "CjvgrHEIycSQ6exznxnFXT",
        svgoTargets: ["icons/o2-new"],
        variants: [
            {
                configName: "o2-new-filled.json",
                frame: "Filled",
                iconsPath: "icons/o2-new/filled",
                script: "export-o2-new-filled",
            },
            {
                configName: "o2-new-regular.json",
                frame: "Regular",
                iconsPath: "icons/o2-new/regular",
                script: "export-o2-new-regular",
            },
            {
                configName: "o2-new-light.json",
                frame: "Light",
                iconsPath: "icons/o2-new/light",
                script: "export-o2-new-light",
            },
        ],
    },
    blau: {
        label: "Blau",
        figmaEnv: "BLAU_FIGMA_ID",
        defaultFileId: "czemeClWRGBI8oF7caNa5m",
        svgoTargets: ["icons/blau"],
        variants: [
            {
                configName: "blau-regular.json",
                frame: "Regular",
                iconsPath: "icons/blau/regular",
                script: "export-blau-regular",
            },
            {
                configName: "blau-filled.json",
                frame: "Filled",
                iconsPath: "icons/blau/filled",
                script: "export-blau-filled",
            },
        ],
    },
    vivo: {
        label: "Vivo",
        figmaEnv: "VIVO_FIGMA_ID",
        defaultFileId: "EApRpjaTyUOwW5VQU2ZqgP",
        svgoTargets: ["icons/vivo-new"],
        variants: [
            {
                configName: "vivo-filled.json",
                frame: "Filled",
                iconsPath: "icons/vivo-new/filled",
                script: "export-vivo-filled",
            },
            {
                configName: "vivo-regular.json",
                frame: "Regular",
                iconsPath: "icons/vivo-new/regular",
                script: "export-vivo-regular",
            },
            {
                configName: "vivo-light.json",
                frame: "Light",
                iconsPath: "icons/vivo-new/light",
                script: "export-vivo-light",
            },
        ],
    },
};

(async () => {
    try {
        const options = parseArgs(process.argv.slice(2));

        if (options.help) {
            printHelp();
            return;
        }

        const brands = resolveBrandSelection(options.brand);
        const token =
            options.token ||
            process.env.FIGMA_TOKEN ||
            process.env.FIGMA_PERSONAL_TOKEN ||
            process.env.MISTICA_FIGMA_TOKEN;

        if (!token) {
            throw new Error(
                "Missing FIGMA_TOKEN. Pass --token <value> or export FIGMA_TOKEN in your shell."
            );
        }

        const template = await loadTemplate();
        const generatedConfigFiles = new Set();

        console.log(
            `Exporting brands: ${brands
                .map((key) => BRANDS[key].label)
                .join(", ")}`
        );

        try {
            for (const brandKey of brands) {
                await prepareConfigsForBrand(
                    brandKey,
                    token,
                    template,
                    generatedConfigFiles
                );
                await runExportsForBrand(brandKey);
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
  --brand <name[,name,...]>   Brand(s) to export (${BRAND_ORDER.join(
      ", "
  )}, or "all")
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
        return [...BRAND_ORDER];
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

    return BRAND_ORDER.filter((brand) => unique.includes(brand));
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
            console.log(`Updated ${path.relative(ROOT, targetPdf)}`);
        }

        await fs.rm(tmpDir, { recursive: true, force: true });
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

    await fs.rename(source, target);
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
    console.log("\nRe-generating markdown catalog");
    await runCommand("python3", [
        ".github/md-generator/generate_markdown.py",
        "icons",
    ]);
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
