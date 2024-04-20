import os

PIPE = "|"
SLASH = "/"
SVG_EXTENSION = ".svg"
PDF_EXTENSION = ".pdf"
BREAK = "\n"

# Show or hide and reorder brands as needed
brands = ["telefonica", "o2", "vivo-new", "blau"]

colors = {
    "unique": "59C2C9",
    "all_equivalence": "0066FF",
    "some_equivalence": "EAC344",
    "missing": "D1D5E4"
}

def preprocess_filename(filename):
    """Normalize filenames by removing specific substrings."""
    return filename.replace("-filled", "").replace("-light", "").replace("-regular", "")

def list_svg_files(folder):
    """List all .svg files in the directory, including subdirectories."""
    svg_files = []
    for root, dirs, files in os.walk(folder):
        svg_files.extend(os.path.join(root, file) for file in files if file.endswith('.svg') and not file.startswith('.'))
    return svg_files

# Llama a la función para obtener la lista de archivos SVG
svg_files = list_svg_files("./icons")

# El total de archivos SVG se obtiene simplemente contando los elementos de la lista retornada
total_icons = len(svg_files)

def process_icon_sets(folders, all_concepts):
    """Process each icon set to compute various metrics, update all_concepts with unique processed names."""
    data = {}
    for folder in folders:
        files = list_svg_files(folder)
        icons = {os.path.basename(file): file for file in files}
        
        # no_processed_names is icons with -regular, -light, -filled
        no_processed_names = {(os.path.basename(file)): file for file in files}

        # processed_names is icons without -regular, -light, -filled
        processed_names = {preprocess_filename(os.path.basename(file)): file for file in files}
        
        data[folder] = {
            "total": len(files),
            "icons": set(icons.keys()),
            "no_processed_names": set(no_processed_names.keys()),
            "processed_names": set(processed_names.keys()),
            "unique": set(),
            "all_equivalence": set(),
            "some_equivalence": set(),
            "missing": set()
        }
        all_concepts.update(data[folder]["no_processed_names"])

    for folder in folders:
        current_no_processed_names = data[folder]["no_processed_names"]
        data[folder]["unique"] = current_no_processed_names - set.union(*(data[f]["no_processed_names"] for f in folders if f != folder))
        data[folder]["all_equivalence"] = set.intersection(*(data[f]["no_processed_names"] for f in folders))
        for other_folder in folders:
            if other_folder != folder:
                data[folder]["some_equivalence"].update(current_no_processed_names & data[other_folder]["no_processed_names"])
        data[folder]["some_equivalence"] -= data[folder]["all_equivalence"]
        data[folder]["missing"] = all_concepts - (data[folder]["unique"] | data[folder]["all_equivalence"] | data[folder]["some_equivalence"])

    return data

def generate_bar_representation(data, folders, bar_width=400, bar_height=8):
    """Generate a color-coded bar representation for each icon set based on percentage data."""
    bar_output = []
    for folder, metrics in data.items():
        folder_data = data[folder]
        total_brand_icons = folder_data['total']
        
        all_equivalence_count = len(folder_data['all_equivalence'])
        all_equivalence_percent = (all_equivalence_count * 100) / total_icons
        some_equivalence_count = len(folder_data['some_equivalence'])
        some_equivalence_percent = (some_equivalence_count * 100) / total_icons
        unique_count = len(folder_data['unique'])
        unique_percent = (unique_count * 100) / total_icons
        missing_count = len(folder_data['missing'])
        missing_percent = (missing_count * 100) / total_icons

        all_equivalence_width = int((all_equivalence_percent / 100) * bar_width)
        if 0 < all_equivalence_percent < 1:
            all_equivalence_width = 2
        some_equivalence_width = int((some_equivalence_percent / 100) * bar_width)
        if 0 < some_equivalence_percent < 1:
            some_equivalence_width = 2
        unique_width = int((unique_percent / 100) * bar_width)
        if 0 < unique_percent < 1:
            unique_width = 2
        missing_width = bar_width - (unique_width + all_equivalence_width + some_equivalence_width)
        
        bar_parts = []
        if all_equivalence_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{all_equivalence_width}x{bar_height}/{colors['all_equivalence']}/000&text=+' alt='All Equivalence'>")
        if some_equivalence_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{some_equivalence_width}x{bar_height}/{colors['some_equivalence']}/000&text=+' alt='Some Equivalence'>")
        if unique_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{unique_width}x{bar_height}/{colors['unique']}/000&text=+' alt='Unique'>")
        if missing_width > 0:
            bar_parts.append(f"<img src='https://dummyimage.com/{missing_width}x{bar_height}/{colors['missing']}/000&text=+' alt='Missing'>")
        
        bar_representation = f"{os.path.basename(folder).title()}  " + "\n" + "".join(bar_parts) + "\n"
        bar_output.append(bar_representation)
    return bar_output

def generate_markdown_table(data, folders, all_concepts):
    """Generate markdown table representation of the data."""
    markdown = "| <sub><sup>ICON SET</sup></sub> | <sub><sup>CONCEPTS</sup></sub> | <sub><sup>TOTAL</sup></sub> | <sub><sup>ALL EQUIVALENCE (%)</sup></sub> | <sub><sup>SOME EQUIVALENCE (%)</sup></sub> | <sub><sup>UNIQUE (%)</sup></sub> | <sub><sup>MISSING</sup></sub> |\n"
    markdown += "| --------- | --------: | -----: | ----------: | -------------------: | -------------------: | ------------: |\n"
    
    for folder in folders:
        folder_name = os.path.basename(folder).title()
        folder_data = data[folder]
        total_concepts = len(all_concepts)
        # print(total_concepts)
        total_brand_icons = folder_data['total']
        # print(total_brand_icons)
        all_equivalence_count = len(folder_data['all_equivalence'])
        all_equivalence_percent = f"{all_equivalence_count} ({all_equivalence_count * 100 / (total_brand_icons):.1f}%) ![All Equivalence](https://dummyimage.com/8x8/{colors['all_equivalence']}/000&text=+)" if total_brand_icons > 0 else "0 (0%)"
        some_equivalence_count = len(folder_data['some_equivalence'])
        some_equivalence_percent = f"{some_equivalence_count} ({some_equivalence_count * 100 / total_brand_icons:.1f}%) ![Some Equivalence](https://dummyimage.com/8x8/{colors['some_equivalence']}/000&text=+)" if total_brand_icons > 0 else "0 (0%)"
        unique_count = len(folder_data['unique'])
        unique_percent = f"{unique_count} ({unique_count * 100 / total_brand_icons:.1f}%) ![Unique](https://dummyimage.com/8x8/{colors['unique']}/000&text=+)" if total_brand_icons > 0 else "0 (0%)"
        missing_count = len(folder_data['missing'])
        missing_percent = f"{missing_count}" #({missing_count * 100 / total_icons:.1f}%)" if total_icons > 0 else "0 (0%)"
        
        markdown += f"| {folder_name} | {len(folder_data['processed_names'])} | {folder_data['total']} | {all_equivalence_percent} | {some_equivalence_percent} | {unique_percent} | {missing_percent} |\n"
    
    markdown += f"| | **{total_concepts}** | **{total_icons}** |  |  |  |  |\n"
    markdown += "\n"
    # markdown += f"<table><tr><th>Total concepts</th><td>{total_concepts}</td></tr><tr><th>Total icons</th><td>{total_icons}</td></tr></table>"
            
    
    return markdown

def read_folder(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        return files
    return []

def generate_icon_table(path):  # Renombrar la función para que coincida con el nombre del módulo
    brands = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    root = os.path.basename(path)
    dictionary = {}
    file_content = BREAK + "| ---BRANDS--- | icon name |" + \
        BREAK + "| ---HEADER-BREAK--- |" + ":--- |" + BREAK
    for brand in brands:
        brand_folder = path + SLASH + brand
        styles = read_folder(brand_folder)
        for style in styles:
            style_folder = brand_folder + SLASH + style
            icons = read_folder(style_folder)
            for icon in icons:
                icon_name = os.path.splitext(icon)[0]
                file_path = root + SLASH + brand + SLASH + \
                    style + SLASH + icon_name + SVG_EXTENSION
                if icon_name in dictionary:
                    if style not in dictionary[icon_name]:
                        dictionary[icon_name][style] = {brand: file_path}
                    else:
                        dictionary[icon_name][style][brand] = file_path
                else:
                    dictionary[icon_name] = {
                        style: {brand: file_path}
                    }

    brands.remove("telefonica")
    brands = ["telefonica"] + sorted(brands, reverse=True)
    separator = " " + PIPE + " "
    file_content = file_content.replace("---BRANDS---", separator.join(brands))
    file_content = file_content.replace("---HEADER-BREAK---", separator.join(
        [":---:"] * (len(brands))))  # add (len(brands) + 2) to add svg & pdf download

    for icon_name in sorted(dictionary.keys()):
        icon = dictionary[icon_name]
        for style in sorted(icon.keys()):
            icon_images = []
            for brand in brands:
                icon_image = "![" + icon_name + \
                    "](" + icon[style][brand] + \
                    ") " if brand in icon[style] else " "
                icon_images.append(icon_image)
            row = PIPE + PIPE.join(icon_images) + PIPE + \
                "<a id=" + "'" + icon_name + "'>"+ "`" + icon_name + "`"  + "</a>" + \
                "[" + "![" + icon_name + "]" + \
                "(.github/resources/anchor.svg)" + \
                "]" + "(" + "#" + icon_name + ")" + PIPE
            file_content += row + BREAK

    return file_content  # Devolver el contenido de la tabla de iconos



def main(root_folder):
    """Main function to orchestrate the icon analysis and reporting."""
    folders = [os.path.join(root_folder, brand) for brand in brands]
    all_concepts = set()
    icon_data = process_icon_sets(folders, all_concepts)
    bars = generate_bar_representation(icon_data, all_concepts)
    
    content_to_write = ""

    # Add documentation
    documentation = "![Mistica Icons](.github/resources/mistica-icons-light.svg#gh-light-mode-only)" + BREAK + "![Mistica Icons](.github/resources/mistica-icons-dark.svg#gh-dark-mode-only)" + BREAK + BREAK + "Mística Icons is a multibrand icon system that contains all icons that is working in [Mistica Design System](https://github.com/Telefonica/mistica) now.  " + BREAK + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10).  " + \
        BREAK + BREAK + "## Documentation" + BREAK + BREAK + "### Develop" + BREAK + BREAK + "#### iOS and Android" + BREAK + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + BREAK + "#### Web" + BREAK + BREAK + \
        "Visit [Mistica Storybook](https://mistica-web.vercel.app/?path=/story/icons-catalog--catalog) to get all the detail about using Mistica Icons Library" + BREAK + BREAK + "### Design" + BREAK + BREAK + "Use Mística icons library in Figma!" + BREAK + BREAK
    content_to_write += documentation + BREAK
    
    # Preparar el contenido total para escribir en el README
    content_to_write += "## Equivalence status\n\n"
    for bar in bars:
        content_to_write += bar + "\n"
    content_to_write += "  " + BREAK

    # Agregar la tabla en formato Markdown al contenido
    markdown_table = generate_markdown_table(icon_data, folders, all_concepts)
    content_to_write += markdown_table + "\n"
    
    legend = (
            "<sub>**Concepts**: Counts the different names of icons in the set excluding any variations in style or weight.</sub>  " 
            + BREAK +
            "<sub>**Total**: The total number of icons found in a brand set. Counting light, regular and filled weights.</sub>  "
            + BREAK +
            "<sub>**All Equivalence**: Icons that are present in all sets.</sub>  " 
            + BREAK +
            "<sub>**Some Equivalence**: Icons that are present in some sets.</sub>  " 
            + BREAK +
            "<sub>**Unique**: Icons that only exists in this set.</sub>  " 
            + BREAK +
            "<sub>**Missing**: Missing icons with respect to other sets.</sub>"
            )

    content_to_write += legend + "\n"
    
    # Agregar el contenido de la tabla de iconos al contenido
    content_to_write += "## Icon equivalence\n\n"
    icon_table_output = generate_icon_table(root_folder)
    content_to_write += icon_table_output + "\n"
    
    # Sobreescribir el archivo README.md con el contenido generado
    with open("./README.md", "w") as file:
        file.write(content_to_write)

if __name__ == "__main__":
    root_folder = "icons"
    main(root_folder)

