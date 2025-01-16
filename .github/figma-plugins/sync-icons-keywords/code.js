// main.js

const documentationLink = "https://github.com/Telefonica/mistica-icons";

// Define the URL of the JSON file (replace with your raw GitHub URL)
const jsonUrl =
    "https://raw.githubusercontent.com/Telefonica/mistica-icons/refs/heads/production/icons/icons-keywords.json";

// Load JSON file content from the provided URL
fetch(jsonUrl)
    .then((response) => {
        if (!response.ok) {
            throw new Error(`The url is not valid: ${jsonUrl}`);
        }
        return response.json();
    })
    .then((data) => {
        // Only load the current page instead of all pages
        const currentPage = figma.currentPage;
        const selection = currentPage.selection;

        // Find components within the selection or entire page (including within frames or groups)
        const scope =
            selection.length > 0
                ? selection.flatMap((node) =>
                      node.findAll
                          ? node.findAll((child) => child.type === "COMPONENT")
                          : node.type === "COMPONENT"
                          ? [node]
                          : []
                  )
                : currentPage
                      .findAll(
                          (node) =>
                              node.type === "COMPONENT" ||
                              node.type === "FRAME" ||
                              node.type === "GROUP"
                      )
                      .flatMap((node) =>
                          node.findAll
                              ? node.findAll(
                                    (child) => child.type === "COMPONENT"
                                )
                              : node.type === "COMPONENT"
                              ? [node]
                              : []
                      )
                      .concat(
                          currentPage.findAll(
                              (node) => node.type === "COMPONENT"
                          )
                      );

        const { updatedCount, totalCount } = syncDescriptions(data, scope);
        figma.closePlugin(
            `Synchronization complete: ${updatedCount} of ${totalCount} components updated.`
        );
    })
    .catch((error) => {
        console.error("Error loading JSON:", error);
        figma.closePlugin(`Error: ${error.message}`);
    });

function syncDescriptions(jsonDescriptions, components) {
    const updatedComponents = []; // Keep track of updated components
    const nonUpdatedComponents = []; // Keep track of non-updated components

    // Process components in batches to improve performance
    const batchSize = 100;
    for (let i = 0; i < components.length; i += batchSize) {
        const batch = components.slice(i, i + batchSize);

        batch.forEach((component) => {
            // Extract the base name by removing known suffixes like -regular, -filled, -light
            const baseName = component.name.replace(
                /-(regular|filled|light)$/,
                ""
            );

            // Debugging: Log the extracted base name and its comparison
            console.log(
                `Processing component: ${component.name}, Base name: ${baseName}`
            );

            // Find matching description in the JSON file
            if (jsonDescriptions[baseName]) {
                // Join all descriptions for the component and update the description
                const descriptions = jsonDescriptions[baseName].join(", ");
                component.description = descriptions;
                component.documentationLinks = [
                    {
                        uri: documentationLink,
                    },
                ];
                updatedComponents.push({
                    name: component.name,
                    description: descriptions,
                });
            } else {
                // If no match, leave the description empty
                component.description = "";
                nonUpdatedComponents.push(component.name);
            }
        });
    }

    // Log the results
    console.log(`Processed ${components.length} components.`);
    console.log(
        `Updated components (${updatedComponents.length}):`,
        updatedComponents
    );
    console.log(
        `Non-updated components (${nonUpdatedComponents.length}):`,
        nonUpdatedComponents
    );

    console.log("Descriptions synchronized successfully");

    return {
        updatedCount: updatedComponents.length,
        totalCount: components.length,
    };
}
