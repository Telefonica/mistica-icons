import os

# Función para preprocesar nombres de archivos de iconos
def preprocess_filename(filename):
    return filename.replace("filled", "").replace("light", "").replace("regular", "")

# Función para contar el total de iconos en una carpeta
def count_total_icons(folder):
    total_icons = 0
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    total_icons += 1
    return total_icons

# Función para contar los iconos únicos en una carpeta
def count_unique_icons(folder):
    icons = set()
    for subfolder in os.listdir(folder):
        subfolder_path = os.path.join(folder, subfolder)
        if os.path.isdir(subfolder_path):
            for filename in os.listdir(subfolder_path):
                if filename.endswith(".svg") and not filename.startswith('.'):
                    icons.add(preprocess_filename(filename))
    return len(icons)

# Función para contar los iconos con equivalencia en una carpeta
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

# Función para contar los iconos con equivalencia en todas las carpetas
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

# Función principal para crear la tabla Markdown
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
    markdown_table = "| Icon Set | Icon Concepts | Total Icons | Icons with All Equivalence | Icons with Equivalence | Unique Icons | Remaining |\n"
    markdown_table += "|:--------|-------------:|--------------:|----------:|------------------------:|---------------------------:|-------------:|\n"
    for label, folder, total_count, unique_count, equivalent_count, all_equivalent_count in zip(labels, folders, total_counts, unique_counts, equivalent_counts, all_equivalent_counts):
        unique_percent = f"{unique_count / total_icons * 100:.1f}%" if total_icons > 0 else "0%"
        equivalent_percent = f"{equivalent_count:.1f}%"
        all_equivalent_percent = f"{all_equivalent_count:.1f}%"
        remaining_percent = f"{100 - float(unique_count / total_icons * 100) - equivalent_count - all_equivalent_count:.1f}%" if total_icons > 0 else "0%"
        markdown_table += f"| {label} | {unique_count} | {total_count} | {all_equivalent_percent} | {equivalent_percent} | {unique_percent} | {remaining_percent} |\n"

    return markdown_table


# Function to create bar representation for each folder
def create_bar_representation(unique_counts, equivalence_percentages, all_equivalence_percentages, total_icons, bar_width=100):
    bar_representation = []

    all_equivalence_color = "0066FF"
    equivalence_color = "EAC344"
    unique_color = "59C2C9"
    remaining_color = "D1D5E4"

    for unique_count, equivalence_percentage, all_equivalence_percentage in zip(unique_counts, equivalence_percentages, all_equivalence_percentages):
        unique_percentage = unique_count / total_icons * 100
        unique_width = max(1, int(unique_percentage * bar_width / 100))  # Width percentage for "Unique Icons"
        equivalence_width = max(1, int(equivalence_percentage * bar_width / 100))  # Width percentage for "Icons with Equivalence"
        all_equivalence_width = max(1, int(all_equivalence_percentage * bar_width / 100))  # Width percentage for "Icons with All Equivalence"
        remaining_width = max(1, bar_width - unique_width - equivalence_width - all_equivalence_width)  # Width percentage for "Remaining"
        
        # Crear la representación de la barra para la carpeta actual
        bar = f"![](https://via.placeholder.com/{all_equivalence_width}x15/{all_equivalence_color}/000000?text=+)" \
              f"![](https://via.placeholder.com/{equivalence_width}x15/{equivalence_color}/000000?text=+)" \
              f"![](https://via.placeholder.com/{unique_width}x15/{unique_color}/000000?text=+)" \
              f"![](https://via.placeholder.com/{remaining_width}x15/{remaining_color}/000000?text=+)"
        
        # Agregar la representación de la barra a la lista
        bar_representation.append(bar)

    return bar_representation


# Run the script
if __name__ == "__main__":
    icons_folder = "icons"
    markdown_table = create_markdown_table(icons_folder)
    print(markdown_table)

    folders = [os.path.join(icons_folder, folder) for folder in os.listdir(icons_folder) if os.path.isdir(os.path.join(icons_folder, folder))]
    labels = [os.path.basename(folder) for folder in folders]

    # Get the percentages for each folder
    unique_percentages = [count_unique_icons(folder) / count_total_icons(folder) * 100 for folder in folders]
    equivalence_percentages = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalence_percentages = [count_all_equivalent_icons(folder, folders) for folder in folders]

    # Get the total counts and unique counts for each folder
    total_counts = [count_total_icons(folder) for folder in folders]
    unique_counts = [count_unique_icons(folder) for folder in folders]

    # Calculate total icons
    total_icons = sum(total_counts)

    # Create bar representation for each folder
    bar_representation = create_bar_representation(unique_counts, equivalence_percentages, all_equivalence_percentages, total_icons, bar_width=200)

    # Print the bar representation
    for label, bar in zip(labels, bar_representation):
        print(f"{label}\n {bar}")

