const BRAND_ORDER = [
    "telefonica",
    "o2",
    "o2-new",
    "blau",
    "vivo",
    "vivo-evolution",
];

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
        svgoTargets: ["icons/vivo"],
        variants: [
            {
                configName: "vivo-filled.json",
                frame: "Filled",
                iconsPath: "icons/vivo/filled",
                script: "export-vivo-filled",
            },
            {
                configName: "vivo-regular.json",
                frame: "Regular",
                iconsPath: "icons/vivo/regular",
                script: "export-vivo-regular",
            },
            {
                configName: "vivo-light.json",
                frame: "Light",
                iconsPath: "icons/vivo/light",
                script: "export-vivo-light",
            },
        ],
    },
    "vivo-evolution": {
        label: "Vivo-evolution",
        figmaEnv: "VIVO_EVOLUTION_FIGMA_ID",
        // TODO: replace with the dedicated Vivo-evolution Figma file id.
        defaultFileId: "REPLACE_WITH_VIVO_EVOLUTION_FILE_ID",
        svgoTargets: ["icons/vivo-evolution"],
        variants: [
            {
                configName: "vivo-evolution-filled.json",
                frame: "Filled",
                iconsPath: "icons/vivo-evolution/filled",
                script: "export-vivo-evolution-filled",
            },
            {
                configName: "vivo-evolution-regular.json",
                frame: "Regular",
                iconsPath: "icons/vivo-evolution/regular",
                script: "export-vivo-evolution-regular",
            },
            {
                configName: "vivo-evolution-light.json",
                frame: "Light",
                iconsPath: "icons/vivo-evolution/light",
                script: "export-vivo-evolution-light",
            },
        ],
    },
};

module.exports = { BRAND_ORDER, BRANDS };
