import os

# Define the desired order of folders
brands = ["telefonica", "o2", "vivo-new", "blau"]

# Define los colores una vez fuera de las funciones
all_equivalence_color = "0066FF"
equivalence_color = "EAC344"
unique_color = "59C2C9"
missing_color = "D1D5E4"

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

def count_missing_icons(folder, all_folders):
    missing = 0
    total_icons = count_total_icons(folder)
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    found_in_all = False
                    for other_folder in all_folders:
                        other_subfolder_path = os.path.join(other_folder, subfolder)
                        if os.path.isdir(other_subfolder_path):
                            if preprocess_filename(filename) in [preprocess_filename(f) for f in os.listdir(other_subfolder_path) if not f.startswith('.')]:
                                found_in_all = True
                                break
                    if not found_in_all:
                        missing += 1
    return missing

def generate_bar_representation(icons_folder):
    bar_width = 500
    
    # Create full paths for the folders in the desired order
    folders = [os.path.join(icons_folder, folder) for folder in brands]
    
    # Extract labels from folder names
    labels = brands
    
    total_counts = [count_total_icons(folder) for folder in folders]
    unique_counts = [count_unique_icons(folder) for folder in folders]
    equivalence_percentages = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalence_percentages = [count_all_equivalent_icons(folder, folders) for folder in folders]
    missing_counts = [count_missing_icons(folder, folders) for folder in folders]  # Calculate missing counts

    total_icons = sum(total_counts)

    bar_representation = []

    for unique_count, equivalence_percentage, all_equivalence_percentage, missing_count in zip(unique_counts, equivalence_percentages, all_equivalence_percentages, missing_counts):
        unique_percentage = unique_count / total_icons * 100
        unique_width = max(1, int(unique_percentage * bar_width / 100))
        equivalence_width = max(1, int(equivalence_percentage * bar_width / 100))
        all_equivalence_width = max(1, int(all_equivalence_percentage * bar_width / 100))
        missing_width = max(1, int((missing_count / total_counts[0]) * bar_width))  # Calculate missing width
        
        bar = f"![](https://dummyimage.com/{all_equivalence_width}x8/{all_equivalence_color}/000000?text=+)" \
              f"![](https://dummyimage.com/{equivalence_width}x8/{equivalence_color}/000000?text=+)" \
              f"![](https://dummyimage.com/{unique_width}x8/{unique_color}/000000?text=+)" \
              f"![](https://dummyimage.com/{missing_width}x8/{missing_color}/000000?text=+)"  # Add missing bar
        
        bar_representation.append(bar)

    # Concatenate bar representation to markdown table content
    bar_content = "\n\n"
    for label, bar in zip(labels, bar_representation):
        bar_content += f"{label}  \n {bar}\n\n"
    
    return bar_content


def icons_equivalence_data_table(root_folder):
    # Crea rutas completas para las carpetas en el orden deseado
    folders = [os.path.join(root_folder, folder) for folder in brands]
    
    # Extrae etiquetas de los nombres de las carpetas
    labels = brands

    unique_counts = [count_unique_icons(folder) for folder in folders]
    equivalent_counts = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalent_counts = [count_all_equivalent_icons(folder, folders) for folder in folders]
    total_counts = [count_total_icons(folder) for folder in folders]
    missing_counts = [count_missing_icons(folder, folders) for folder in folders]  # Calculate missing counts

    total_icons = sum(total_counts)

    markdown_table = "<br/>\n"
    markdown_table += f"\n| Icon Set | Concepts | Total | All Equivalence | Some Equivalence | Unique | Missing |\n"
    markdown_table += "|:--------|-------------:|--------------:|----------:|------------------------:|---------------------------:|-------------:|\n"
    for label, folder, total_count, unique_count, equivalent_count, all_equivalent_count, missing_count in zip(labels, folders, total_counts, unique_counts, equivalent_counts, all_equivalent_counts, missing_counts):
        unique_percent = f"{unique_count / total_icons * 100:.1f}%" + f" ![](https://dummyimage.com/8x8/{unique_color}/000000?text=+)" if total_icons > 0 else "0%"
        equivalent_percent = f"{equivalent_count:.1f}%" + f" ![](https://dummyimage.com/8x8/{equivalence_color}/000000?text=+)"
        all_equivalent_percent = f"{all_equivalent_count:.1f}%" + f" ![](https://dummyimage.com/8x8/{all_equivalence_color}/000000?text=+) "
        missing_percent = f"{missing_count / total_count * 100:.1f}%" + f" ![](https://dummyimage.com/8x8/{missing_color}/000000?text=+) "  # Calculate missing percent
        markdown_table += f"| {label} | {unique_count} | {total_count} | {all_equivalent_percent} | {equivalent_percent} | {unique_percent} | {missing_percent} |\n"
        print(f"Icon Set: {label}")
        print(f"Total Concepts: {unique_count}")
        print(f"Total Icons: {total_count}")
        print(f"All Equivalence: {all_equivalent_percent}")
        print(f"Some Equivalence: {equivalent_percent}")
        print(f"Unique: {unique_percent}")
        print(f"Missing: {missing_percent}")
        print("\n")

    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Icon Set:** The name of the brand being analyzed."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Concepts:** The number of unique icons in the set, i.e., those icons whose names do not repeat within the same brand."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Total:** The total number of icons found in a brand set. Counting light, regular and filled weights."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**All Equivalence:** The percentage of icons that have equivalence in all icon sets, relative to the total number of icons in a specific set."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Some Equivalence:** The percentage of icons that have at least one equivalence with another icon in some other set, relative to the total number of icons in the set."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Unique:** The percentage of unique icons relative to the total number of icons in the this set."
    markdown_table += "</sub>  "
    markdown_table += "\n"
    markdown_table += "<sub>"
    markdown_table += "**Missing:** The missing percentage of icons after taking into account unique icons, icons with some equivalence, and icons with equivalence in all sets. This percentage represents the icons that do not fall into any of these categories."
    markdown_table += "</sub>"
    markdown_table += "\n\n"

    return markdown_table

root_folder = "icons"
print("Bar Representation:")
print(generate_bar_representation(root_folder))
print("\nIcons Equivalence Data Table:")
print(icons_equivalence_data_table(root_folder))
