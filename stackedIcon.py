import os

# Function to preprocess icon filenames
def preprocess_filename(filename):
    return filename.replace("filled", "").replace("light", "").replace("regular", "")

# Function to count total icons in a folder
def count_total_icons(folder):
    total_icons = 0
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    total_icons += 1
    return total_icons

# Function to count unique icons in a folder
def count_unique_icons(folder):
    icons = set()
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    icons.add(preprocess_filename(filename))
    return len(icons)

# Function to count icons with equivalence
def count_equivalent_icons(folder, all_folders):
    equivalent = 0
    total_icons = count_total_icons(folder)
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    for other_folder in all_folders:
                        if other_folder != folder:
                            other_subfolder_path = os.path.join(other_folder, subfolder)
                            if os.path.isdir(other_subfolder_path):
                                if preprocess_filename(filename) in [preprocess_filename(f) for f in os.listdir(other_subfolder_path) if not f.startswith('.')]:
                                    equivalent += 1
                                    break
    return f"{equivalent / total_icons * 100:.1f}%" if total_icons > 0 else "0%"

# Function to count icons with equivalence in all folders
def count_all_equivalent_icons(folder, all_folders):
    all_equivalent = 0
    total_icons = count_total_icons(folder)
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    found_in_all = True
                    for other_folder in all_folders:
                        other_subfolder_path = os.path.join(other_folder, subfolder)
                        if os.path.isdir(other_subfolder_path):
                            if preprocess_filename(filename) not in [preprocess_filename(f) for f in os.listdir(other_subfolder_path) if not f.startswith('.')]:
                                found_in_all = False
                                break
                    if found_in_all:
                        all_equivalent += 1
    return f"{all_equivalent / total_icons * 100:.1f}%" if total_icons > 0 else "0%"

# Main function to create markdown table
def create_markdown_table(root_folder):
    folders = [os.path.join(root_folder, folder) for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]
    labels = [os.path.basename(folder) for folder in folders]

    icon_concepts = [count_unique_icons(folder) for folder in folders]
    equivalent_counts = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalent_counts = [count_all_equivalent_icons(folder, folders) for folder in folders]
    total_counts = [count_total_icons(folder) for folder in folders]

    # Calculate total icons
    total_icons = sum(total_counts)

    # Create markdown table
    markdown_table = "| Folder | Icon Concepts |Total Icons | Icons with Equivalence | Icons with All Equivalence | Remaining |\n"
    markdown_table += "|:--------|-------------:|--------------:|------------------------:|---------------------------:|-------------:|\n"
    for label, folder, total_count, icon_concept, equivalent_count, all_equivalent_count in zip(labels, folders, total_counts, icon_concepts, equivalent_counts, all_equivalent_counts):
        remaining_percent = 100 - float(icon_concept / total_icons * 100) - float(equivalent_count[:-1]) - float(all_equivalent_count[:-1])
        remaining_percent = f"{remaining_percent:.1f}%" if remaining_percent > 0 else "0%"
        markdown_table += f"| {label} | {icon_concept}  |{total_count} | {equivalent_count} | {all_equivalent_count} | {remaining_percent} |\n"

    return markdown_table

# Run the script
if __name__ == "__main__":
    icons_folder = "icons"
    markdown_table = create_markdown_table(icons_folder)
    print(markdown_table)
