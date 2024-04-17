# generate_markdown.py

import os
import sys
from generate_icon_table import generate_icon_table
from generate_graph import create_bar_representation, icons_equivalence_data_table, count_total_icons, count_unique_icons, count_equivalent_icons, count_all_equivalent_icons

def generate_bar_representation(icons_folder):
    folders = [os.path.join(icons_folder, folder) for folder in os.listdir(icons_folder) if os.path.isdir(os.path.join(icons_folder, folder))]
    labels = [os.path.basename(folder) for folder in folders]
    total_counts = [count_total_icons(folder) for folder in folders]
    unique_counts = [count_unique_icons(folder) for folder in folders]
    equivalence_percentages = [count_equivalent_icons(folder, folders) for folder in folders]
    all_equivalence_percentages = [count_all_equivalent_icons(folder, folders) for folder in folders]
    total_icons = sum(total_counts)
    bar_representation = create_bar_representation(unique_counts, equivalence_percentages, all_equivalence_percentages, total_icons)

    # Concatenate bar representation to markdown table content
    bar_content = ""
    bar_content += "\n\n"
    bar_content += "## Equivalence status\n\n"
    for label, bar in zip(labels, bar_representation):
        bar_content += f"{label}  \n {bar}\n\n"
    
    return bar_content

def main():
    BREAK = "\n"

    if len(sys.argv) < 2:
        print("Usage: python generate_markdown.py /path/to/icons/folder")
        sys.exit(1)

    icons_folder = sys.argv[1]
    output_file_path = "./README.md"

    # Documentation
    documentation = "![Mistica Icons](.github/resources/mistica-icons-light.svg#gh-light-mode-only)" + BREAK + "![Mistica Icons](.github/resources/mistica-icons-dark.svg#gh-dark-mode-only)" + BREAK + BREAK + "## What is this?  " + BREAK + BREAK + "Mística Icons is a multibrand icon system that contains all icons that is working in [Mistica Design System](https://github.com/Telefonica/mistica) now.  " + BREAK + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10).  " + \
        BREAK + BREAK + "## Documentation" + BREAK + BREAK + "### Develop" + BREAK + BREAK + "#### iOS and Android" + BREAK + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + BREAK + "#### Web" + BREAK + BREAK + \
        "Visit [Mistica Storybook](https://mistica-web.vercel.app/?path=/story/icons-catalog--catalog) to get all the detail about using Mistica Icons Library" + BREAK + BREAK + "### Design" + BREAK + BREAK + "Use Mística icons library in Figma!" + BREAK + BREAK

    # Generate bar representation
    bar_content = generate_bar_representation(icons_folder)
    
    # Generate markdown table content
    markdown_table_content = icons_equivalence_data_table(icons_folder)

    # Generate icon table content
    icon_table_content = generate_icon_table(icons_folder)

    # Print or write the contents to the output file
    with open(output_file_path, "w+") as file:
        file.write(documentation)
        file.write(bar_content)
        file.write(markdown_table_content)
        file.write(icon_table_content)
        # You can also print the contents if needed
        # print(icon_table_content)
        # print(markdown_table_content)

if __name__ == "__main__":
    main()
