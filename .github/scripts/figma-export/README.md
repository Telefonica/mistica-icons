# Figma Export Script

This directory hosts the Node.js entry point that powers both the local export command (`yarn figma-export`) and the GitHub Actions workflow. Use it whenever you need to pull the latest icons from Figma or re-run the post-processing pipeline (SVGO, PDF conversion, README regeneration).

## Usage

From the repository root:

```bash
yarn figma-export [options]
```

To export directly with figma token

```bash
yarn figma-export [options] --token your_figma_token
```

## Flags

| Flag                    | What it does                                                                                          | Example                              |
| ----------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------ |
| `--brand <value>`       | Restrict export to specific brands (`telefonica`, `o2`, `o2-new`, `blau`, `vivo`) or `all` (default). | `yarn figma-export --brand blau,o2`  |
| `--token <FIGMA_TOKEN>` | Provide a token explicitly instead of relying on `FIGMA_TOKEN` env/.env.                              | `yarn figma-export --token figd_xxx` |
| `--skip-export`         | Skip the Figma download step and only run SVGO/PDF/README post-processing.                            | `yarn figma-export --skip-export`    |
| `--skip-svgo`           | Skip SVGO optimization if you already processed SVGs.                                                 | `yarn figma-export --skip-svgo`      |
| `--skip-pdf`            | Skip SVG→PDF conversion.                                                                              | `yarn figma-export --skip-pdf`       |
| `--skip-readme`         | Skip README/ICON_TABLE regeneration.                                                                  | `yarn figma-export --skip-readme`    |

Run `yarn figma-export --help` for the complete option list.

**Important:** Figma Token is mandatory to use export feature.

## What the script does

1. Generates temporary figma-export config files per brand/weight and calls the corresponding `npm run export-*` scripts.
2. Optimizes the resulting SVGs via SVGO (respecting `svgo.config.js`).
3. Converts SVGs to deterministically generated PDFs (requires `librsvg`, `exiftool`, `qpdf`).
4. Regenerates `README.md` and `ICON_TABLE.md` through `.github/scripts/md-generator/generate_markdown.py`.

If any of these steps are not needed in your run, pair the command with the matching `--skip-*` flag.

## Requirements

- Node.js 18+ and Yarn (already handled in CI).
- System binaries: `librsvg` (`rsvg-convert`), `exiftool`, `qpdf`.
- Valid Figma personal access token stored in `.env` or the shell.

With those in place, the script can fully mirror the CI export locally or inside GitHub Actions containers.
