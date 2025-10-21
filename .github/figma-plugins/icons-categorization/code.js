// Figma plugin to organize icons by categories
// Based on descriptions with format "Category: [name]"

// Function to extract category from description
function extractCategory(description) {
    if (!description) {
        console.log("No description available");
        return "Uncategorized";
    }

    console.log(`Searching for category in: "${description}"`);

    // Search for "Category: [name]" pattern case-insensitive
    const categoryMatch = description.match(/Category:\s*([^,\n\r]+)/i);

    if (categoryMatch) {
        const category = categoryMatch[1].trim();
        console.log(`Category found: "${category}"`);
        return category;
    } else {
        console.log("'Category:' pattern not found in description");
        return "Uncategorized";
    }
}

// Function to group instances by category
function groupInstancesByCategory(instances) {
    const groups = new Map();

    instances.forEach((instance) => {
        // Get instance description
        const description = instance.description || "";
        console.log(
            `Instance: ${instance.name}, Description: "${description}"`
        );

        const category = extractCategory(description);
        console.log(`Extracted category: "${category}"`);

        if (!groups.has(category)) {
            groups.set(category, []);
        }
        groups.get(category).push(instance);
    });

    // Log summary of found categories
    console.log("\n=== CATEGORIES SUMMARY ===");
    for (const [categoryName, categoryInstances] of groups) {
        console.log(
            `Category: "${categoryName}" - ${categoryInstances.length} instances`
        );
    }

    return groups;
}

// Function to create a text title for a category
function createCategoryTitle(categoryName, x, y) {
    const textNode = figma.createText();
    textNode.fontName = { family: "Roboto", style: "Regular" };
    textNode.characters = categoryName;
    textNode.x = x;
    textNode.y = y;
    textNode.fontSize = 24;

    return textNode;
}

// Main function to organize icons
async function organizeIconsByCategory() {
    // Check that elements are selected
    if (figma.currentPage.selection.length === 0) {
        figma.notify("Please select the icon instances you want to organize");
        return;
    }

    // Load default Figma font
    await figma.loadFontAsync({ family: "Roboto", style: "Regular" });

    const selectedInstances = figma.currentPage.selection;

    // Filter only instances
    const instances = selectedInstances.filter(
        (node) => node.type === "INSTANCE" || node.type === "COMPONENT"
    );

    if (instances.length === 0) {
        figma.notify("No instances or components found in selection");
        return;
    }

    // Group instances by category
    const categoryGroups = groupInstancesByCategory(instances);

    // Layout configuration
    const TITLE_HEIGHT = 40;
    const ICON_SIZE = 64; // Estimated icon size
    const SPACING_X = 80; // Horizontal spacing between icons
    const SPACING_Y = 80; // Vertical spacing between icons
    const CATEGORY_SPACING = 120; // Spacing between categories
    const ICONS_PER_ROW = 8; // Number of icons per row

    let currentY = 0;
    const startX = 0;

    // Organize each category
    for (const [categoryName, categoryInstances] of categoryGroups) {
        // Create category title
        const titleNode = createCategoryTitle(categoryName, startX, currentY);
        figma.currentPage.appendChild(titleNode);

        currentY += TITLE_HEIGHT + 20; // Space after title

        // Organize icons of this category in a grid
        categoryInstances.forEach((instance, index) => {
            const row = Math.floor(index / ICONS_PER_ROW);
            const col = index % ICONS_PER_ROW;

            const x = startX + col * SPACING_X;
            const y = currentY + row * SPACING_Y;

            instance.x = x;
            instance.y = y;
        });

        // Calculate height used by this category
        const rows = Math.ceil(categoryInstances.length / ICONS_PER_ROW);
        const categoryHeight = rows * SPACING_Y;

        currentY += categoryHeight + CATEGORY_SPACING;
    }

    // Show summary
    const totalCategories = categoryGroups.size;
    const totalInstances = instances.length;

    figma.notify(
        `Organized ${totalInstances} icons in ${totalCategories} categories`
    );

    // Show details of found categories
    console.log("Categories found:");
    for (const [categoryName, categoryInstances] of categoryGroups) {
        console.log(`- ${categoryName}: ${categoryInstances.length} icons`);
    }
}

// Execute plugin
organizeIconsByCategory()
    .then(() => {
        figma.closePlugin();
    })
    .catch((error) => {
        console.error("Error organizing icons:", error);
        figma.notify("Error: " + error.message);
        figma.closePlugin();
    });
