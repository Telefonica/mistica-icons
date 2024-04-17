import os

def preprocess_filename(filename):
    return filename.replace("filled", "").replace("light", "").replace("regular", "")

def count_total_icons(folder):
    total_icons = 0
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    total_icons += 1
    return total_icons

def count_unique_icons(folder):
    icons = set()
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    icons.add(preprocess_filename(filename))
    return len(icons)

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
    return equivalent / total_icons * 100 if total_icons > 0 else 0

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
    return all_equivalent / total_icons * 100 if total_icons > 0 else 0

def create_bar_representation(unique_counts, equivalence_percentages, all_equivalence_percentages, total_icons):
    bar_width = 500
    
    bar_representation = []

    all_equivalence_color = "0066FF"
    equivalence_color = "EAC344"
    unique_color = "59C2C9"
    remaining_color = "D1D5E4"

    for unique_count, equivalence_percentage, all_equivalence_percentage in zip(unique_counts, equivalence_percentages, all_equivalence_percentages):
        unique_percentage = unique_count / total_icons * 100
        unique_width = max(1, int(unique_percentage * bar_width / 100))
        equivalence_width = max(1, int(equivalence_percentage * bar_width / 100))
        all_equivalence_width = max(1, int(all_equivalence_percentage * bar_width / 100))
        remaining_width = max(1, bar_width - unique_width - equivalence_width - all_equivalence_width)
        
        bar = f"![](https://dummyimage.com/{all_equivalence_width}x8/{all_equivalence_color}/000000?text=+)" \
              f"![](https://dummyimage.com/{equivalence_width}x8/{equivalence_color}/000000?text=+)" \
              f"![](https://dummyimage.com/{unique_width}x8/{unique_color}/000000?text=+)" \
              f"![](https://dummyimage.com/{remaining_width}x8/{remaining_color}/000000?text=+)"
        
        bar_representation.append(bar)

    return bar_representation


def icons_equivalence_data_table(root_folder):
    folders = [os.path.join(root_folder, folder) for folder in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, folder))]
    labels = [os.path.basename(folder) for folder in folders]

    unique_counts = [count_unique_icons(folder) for folder in folders]
    equivalent_counts = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalent_counts = [count_all_equivalent_icons(folder, folders) for folder in folders]
    total_counts = [count_total_icons(folder) for folder in folders]

    total_icons = sum(total_counts)

    markdown_table = "<br/>\n"
    markdown_table += "\n| Icon Set | Icon Concepts | Total Icons | Icons with All Equivalence | Icons with Equivalence | Unique Icons | Remaining |\n"
    markdown_table += "|:--------|-------------:|--------------:|----------:|------------------------:|---------------------------:|-------------:|\n"
    for label, folder, total_count, unique_count, equivalent_count, all_equivalent_count in zip(labels, folders, total_counts, unique_counts, equivalent_counts, all_equivalent_counts):
        unique_percent = f"{unique_count / total_icons * 100:.1f}%" if total_icons > 0 else "0%"
        equivalent_percent = f"{equivalent_count:.1f}%"
        all_equivalent_percent = f"{all_equivalent_count:.1f}%"
        remaining_percent = f"{100 - float(unique_count / total_icons * 100) - equivalent_count - all_equivalent_count:.1f}%" if total_icons > 0 else "0%"
        markdown_table += f"| {label} | {unique_count} | {total_count} | {all_equivalent_percent} | {equivalent_percent} | {unique_percent} | {remaining_percent} |\n"

    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Icon Set:** The name of the brand or folder being analyzed."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Icon Concepts:** The number of unique icons in the set, i.e., those icons whose names do not repeat within the same brand."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Total Icons:** The total number of icons found in the folder."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Icons with All Equivalence:** The percentage of icons that have equivalence in all icon sets, relative to the total number of icons in a specific set."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Icons with Equivalence:** The percentage of icons that have at least one equivalence with another icon in some other brand, relative to the total number of icons in the folder."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Unique Icons:** The percentage of unique icons relative to the total number of icons in the folder."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Remaining:** The remaining percentage of icons after taking into account unique icons, icons with equivalence, and icons with equivalence in all folders. This percentage represents the icons that do not fall into any of these categories."
    markdown_table += "</sub>"
    markdown_table += "\n\n"
    markdown_table += "---"

    return markdown_table

