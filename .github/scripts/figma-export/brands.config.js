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
        defaultFileId: "CjvgrHEIycSQ6exznxnFXT",
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
    "vivo-evolution": {
         label: "Vivo-evolution",
         figmaEnv: "VIVO_EVOLUTION_FIGMA_ID",
         defaultFileId: null,
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

module.exports = { BRANDS };
