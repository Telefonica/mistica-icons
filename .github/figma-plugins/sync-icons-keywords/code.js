// main.js

const branch = "production";
const documentationLink = "https://github.com/Telefonica/mistica-icons";

// Define the URL of the JSON file (replace with your raw GitHub URL)
const jsonUrl = `https://raw.githubusercontent.com/Telefonica/mistica-icons/refs/heads/${branch}/icons/icons-keywords.json`;

// Load JSON file content from the provided URL
fetch(jsonUrl)
    .then((response) => {
        console.log("Fetch response status:", response.status);
        if (!response.ok) {
            throw new Error(`The url is not valid: ${jsonUrl}`);
        }
        return response.json();
    })
    .then((data) => {
        console.log(
            "JSON data loaded successfully:",
            Object.keys(data).length,
            "entries"
        );

        // Only load the current page instead of all pages
        const currentPage = figma.currentPage;
        const selection = currentPage.selection;
        console.log("Current page:", currentPage.name);
        console.log("Selection count:", selection.length);

        let components = [];

        if (selection.length > 0) {
            // Process selection
            console.log("Processing selection...");
            selection.forEach((node) => {
                if (node.type === "COMPONENT") {
                    components.push(node);
                } else if (node.findAll) {
                    const foundComponents = node.findAll(
                        (child) => child.type === "COMPONENT"
                    );
                    components.push(...foundComponents);
                }
            });
        } else {
            // Process entire page
            console.log("Processing entire page...");
            components = currentPage.findAll(
                (node) => node.type === "COMPONENT"
            );
        }

        console.log("Found components:", components.length);
        components.forEach((component) => {
            console.log("Component found:", component.name);
        });

        const { updatedCount, totalCount, errorCount } = syncDescriptions(
            data,
            components
        );

        let message = `Sync completed: ${updatedCount} of ${totalCount} components updated.`;
        if (errorCount > 0) {
            message += ` ${errorCount} errors encountered - check console for details.`;
        }

        figma.closePlugin(message);
    })
    .catch((error) => {
        console.error("Error loading JSON:", error);
        console.error("Error details:", {
            message: error.message,
            stack: error.stack,
            url: jsonUrl,
        });

        // Provide more detailed error information
        let errorMessage = `Error: ${error.message}`;
        if (error.message.includes("fetch")) {
            errorMessage +=
                "\n\nPossible causes:\n1. Network connectivity issues\n2. GitHub repository access problems\n3. CORS policy restrictions";
        }

        figma.closePlugin(errorMessage);
    });

function syncDescriptions(jsonDescriptions, components) {
    // console.log(
    //     "Starting synchronization with",
    //     components.length,
    //     "components"
    // );

    const updatedComponents = []; // Keep track of updated components
    const nonUpdatedComponents = []; // Keep track of non-updated components
    const errorComponents = []; // Keep track of components with errors

    // Process components in batches to improve performance
    const batchSize = 100;
    for (let i = 0; i < components.length; i += batchSize) {
        const batch = components.slice(i, i + batchSize);
        console.log(
            `Processing batch ${
                Math.floor(i / batchSize) + 1
            }, components ${i} to ${Math.min(i + batchSize, components.length)}`
        );

        batch.forEach((component, index) => {
            try {
                // Extract the base name by removing known suffixes like -regular, -filled, -light
                const baseName = component.name.replace(
                    /-(regular|filled|light)$/,
                    ""
                );

                // console.log(
                //     `[${i + index + 1}/${components.length}] Processing: ${
                //         component.name
                //     } -> Base: ${baseName}`
                // );

                // Find matching description in the JSON file
                if (jsonDescriptions[baseName]) {
                    const iconData = jsonDescriptions[baseName];

                    // Validate the structure of the icon data
                    if (typeof iconData !== "object" || iconData === null) {
                        console.warn(
                            `⚠ Unexpected data structure for ${baseName}:`,
                            iconData
                        );
                        nonUpdatedComponents.push({
                            name: component.name,
                            baseName: baseName,
                            reason: "Invalid data structure",
                        });
                        return;
                    }

                    // Create description with category and keywords
                    let description = "";
                    if (iconData.category) {
                        description += `Category: ${iconData.category}\n\n`;
                    }
                    if (iconData.keywords && Array.isArray(iconData.keywords)) {
                        description += iconData.keywords.join(", ");
                    } else if (iconData.keywords) {
                        console.warn(
                            `⚠ Keywords for ${baseName} are not an array:`,
                            iconData.keywords
                        );
                        description += String(iconData.keywords);
                    }

                    // Check if component is editable
                    if (component.description !== undefined) {
                        component.description = description;
                        component.documentationLinks = [
                            {
                                uri: documentationLink,
                            },
                        ];

                        console.log(
                            `✓ Updated: ${component.name} with category: ${
                                iconData.category || "N/A"
                            } and description: ${description.substring(
                                0,
                                80
                            )}...`
                        );

                        updatedComponents.push({
                            name: component.name,
                            description: description,
                            category: iconData.category || "N/A",
                        });
                    } else {
                        console.error(
                            `✗ Cannot update ${component.name}: description property not available`
                        );
                        errorComponents.push({
                            name: component.name,
                            error: "description property not available",
                        });
                    }
                } else {
                    // If no match, leave the description empty
                    if (component.description !== undefined) {
                        component.description = "";
                        console.log(
                            `○ No match for: ${component.name} (base: ${baseName}) - cleared description`
                        );
                    }
                    nonUpdatedComponents.push({
                        name: component.name,
                        baseName: baseName,
                        reason: "No JSON match found",
                    });
                }
            } catch (error) {
                console.error(
                    `Error processing component ${component.name}:`,
                    error
                );
                errorComponents.push({
                    name: component.name,
                    error: error.message,
                });
            }
        });
    }

    // Log the results
    console.log(`\n=== SYNCHRONIZATION RESULTS ===`);
    console.log(`Total components processed: ${components.length}`);
    console.log(`Successfully updated: ${updatedComponents.length}`);
    console.log(`No matches found: ${nonUpdatedComponents.length}`);
    console.log(`Errors encountered: ${errorComponents.length}`);

    // Show categories statistics
    if (updatedComponents.length > 0) {
        const categoriesCount = {};
        updatedComponents.forEach((c) => {
            categoriesCount[c.category] =
                (categoriesCount[c.category] || 0) + 1;
        });
        console.log(`\nCategories found:`, categoriesCount);
    }

    if (updatedComponents.length > 0) {
        console.log(
            `\nUpdated components:`,
            updatedComponents.map((c) => `${c.name} (${c.category})`)
        );
    }

    if (nonUpdatedComponents.length > 0) {
        console.log(`\nNon-updated components:`, nonUpdatedComponents);
    }

    if (errorComponents.length > 0) {
        console.log(`\nError components:`, errorComponents);
    }

    console.log("Descriptions synch successfully");

    return {
        updatedCount: updatedComponents.length,
        totalCount: components.length,
        errorCount: errorComponents.length,
    };
}
