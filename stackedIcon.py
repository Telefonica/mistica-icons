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
                if filename.endswith(".svg"):
                    total_icons += 1
    return total_icons

# Function to count unique icons in a folder
def count_unique_icons(folder):
    icons = set()
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg"):
                    icons.add(preprocess_filename(filename))
    return len(icons)

# Function to count icons with equivalence
def count_equivalent_icons(folder, all_folders):
    equivalent = 0
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg"):
                    for other_folder in all_folders:
                        if other_folder != folder:
                            other_subfolder_path = os.path.join(other_folder, subfolder)
                            if os.path.isdir(other_subfolder_path):
                                if preprocess_filename(filename) in [preprocess_filename(f) for f in os.listdir(other_subfolder_path)]:
                                    equivalent += 1
                                    break
    return equivalent

# Function to count icons with equivalence in all folders
def count_all_equivalent_icons(folder, all_folders):
    all_equivalent = 0
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg"):
                    found_in_all = True
                    for other_folder in all_folders:
                        other_subfolder_path = os.path.join(other_folder, subfolder)
                        if os.path.isdir(other_subfolder_path):
                            if preprocess_filename(filename) not in [preprocess_filename(f) for f in os.listdir(other_subfolder_path)]:
                                found_in_all = False
                                break
                    if found_in_all:
                        all_equivalent += 1
    return all_equivalent

# Main function to create markdown table
def create_markdown_table(root_folder):
    folders = [os.path.join(root_folder, folder) for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]
    labels = [os.path.basename(folder) for folder in folders]

    unique_counts = [count_unique_icons(folder) for folder in folders]
    equivalent_counts = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalent_counts = [count_all_equivalent_icons(folder, folders) for folder in folders]
    total_counts = [count_total_icons(folder) for folder in folders]

    # Calculate total icons
    total_icons = sum(total_counts)

    # Create markdown table
    markdown_table = "| Folder | Total Icons | Unique Icons | Icons with Equivalence | Icons with All Equivalence | Unique % | Equivalence % | All Equivalence % | Remaining % |\n"
    markdown_table += "|--------|-------------|--------------|------------------------|---------------------------|----------|---------------|------------------|-------------|\n"
    for label, total_count, unique_count, equivalent_count, all_equivalent_count in zip(labels, total_counts, unique_counts, equivalent_counts, all_equivalent_counts):
        unique_percent = unique_count / total_count * 100 if total_count > 0 else 0
        equivalent_percent = equivalent_count / total_count * 100 if total_count > 0 else 0
        all_equivalent_percent = all_equivalent_count / total_count * 100 if total_count > 0 else 0
        remaining_percent = 100 - (unique_percent + equivalent_percent + all_equivalent_percent)
        markdown_table += f"| {label} | {total_count} | {unique_count} | {equivalent_count} | {all_equivalent_count} | {unique_percent:.2f}% | {equivalent_percent:.2f}% | {all_equivalent_percent:.2f}% | {remaining_percent:.2f}% |\n"

    return markdown_table

# Run the script
if __name__ == "__main__":
    icons_folder = "icons"
    markdown_table = create_markdown_table(icons_folder)
    print(markdown_table)
