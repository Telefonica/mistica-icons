# !/usr/bin/python

import os
import sys

PIPE = "|"
SLASH = "/"
SVG_EXTENSION = ".svg"
PDF_EXTENSION = ".pdf"
BREAK = "\n"

BAR_FILLED = "![bar_filled](.github/resources/filled.png)"
BAR_EMPTY = "![bar_empty](.github/resources/empty.png)"

BAR_FILLED_S = "![bar_filled](.github/resources/filled-s.png)"
BAR_EMPTY_S = "![bar_empty](.github/resources/empty-s.png)"

def read_folder(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        return files
    return []

# List of all icons per brand
icons_telefonica = set()
icons_o2 = set()
icons_blau = set()
icons_vivo = set()

# Adding icons to each list
def add_icons_from_folder(folder_name, icon_set):
    for root, dirs, files in os.walk(f'icons/{folder_name}/'):
        for file in files:
            if file.endswith(".svg"):
                icon_set.add(file)

add_icons_from_folder('telefonica', icons_telefonica)
add_icons_from_folder('o2', icons_o2)
add_icons_from_folder('blau', icons_blau)
add_icons_from_folder('vivo', icons_vivo)

# Length of brand lists
len_icons_telefonica = len(icons_telefonica)
len_icons_o2 = len(icons_o2)
len_icons_blau = len(icons_blau)
len_icons_vivo = len(icons_vivo)

# Union of all icons (no repeated!)
total_icons = sorted(set.union(icons_telefonica, icons_o2, icons_blau, icons_vivo))

# Total icons in integer format
len_total_icons = len(total_icons) 

# Intersections lists in integer format
telefonica_intersection = icons_telefonica & (icons_blau | icons_o2 | icons_vivo)
o2_intersection = icons_o2 & (icons_blau | icons_telefonica | icons_vivo)
blau_intersection = icons_blau & (icons_telefonica | icons_o2 | icons_vivo)
vivo_intersection = icons_blau & (icons_telefonica | icons_o2 | icons_blau)

# —————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————

# Calculate the length of the intersection of each set with the union of the other two sets
telefonica_local_equivalence = len(icons_telefonica & (icons_o2 | icons_blau | icons_vivo))
o2_local_equivalence = len(icons_o2 & (icons_telefonica | icons_blau | icons_vivo))
blau_local_equivalence = len(icons_blau & (icons_telefonica | icons_o2 | icons_vivo))
vivo_local_equivalence = len(icons_vivo & (icons_telefonica | icons_o2 | icons_blau))

# Calculate the local percentage for each set
telefonica_local_percentage = int(100 * telefonica_local_equivalence / len(icons_telefonica))
o2_local_percentage = int(100 * o2_local_equivalence / len(icons_o2))
blau_local_percentage = int(100 * blau_local_equivalence / len(icons_blau))
vivo_local_percentage = int(100 * vivo_local_equivalence / len(icons_vivo))

# LOCAL BARS
# Define a helper function to calculate the local bar
def calculate_local_bar(local_percentage):
    # Calculate the number of filled and empty bars needed
    num_filled_bars = int(local_percentage / 10) * 2
    num_empty_bars = abs(int(local_percentage / 10) - 10) * 2
    # Construct and return the local bar
    return num_filled_bars * BAR_FILLED + num_empty_bars * BAR_EMPTY

# Calculate the local bar for each set
telefonica_local_bar = calculate_local_bar(telefonica_local_percentage)
o2_local_bar = calculate_local_bar(o2_local_percentage)
blau_local_bar = calculate_local_bar(blau_local_percentage)
vivo_local_bar = calculate_local_bar(vivo_local_percentage)

# Composition of LOCAL (X / Y) for markdown
# Define a helper function to calculate the local comparison string
def calculate_local_comparison(local_equivalence, total_icons):
    return f" ({local_equivalence} / {len(total_icons)})"

# Calculate the local comparison string for each set
comp_local_telefonica = calculate_local_comparison(telefonica_local_equivalence, icons_telefonica)
comp_local_o2 = calculate_local_comparison(o2_local_equivalence, icons_o2)
comp_local_blau = calculate_local_comparison(blau_local_equivalence, icons_blau)
comp_local_vivo = calculate_local_comparison(vivo_local_equivalence, icons_vivo)

# Composition of LOCAL BAR + (X / Y) for markdown
# Define a helper function to calculate the local comparison string
def calculate_local_string(name, local_bar, local_percentage, local_comparison):
    return f"{name} set  {BREAK}{local_bar}    {local_percentage}%{local_comparison} `local`  "

# Calculate the local string for each set
telefonica_local = calculate_local_string("Telefónica", telefonica_local_bar, telefonica_local_percentage, comp_local_telefonica)
o2_local = calculate_local_string("O₂", o2_local_bar, o2_local_percentage, comp_local_o2)
blau_local = calculate_local_string("Blau", blau_local_bar, blau_local_percentage, comp_local_blau)
vivo_local = calculate_local_string("Vivo", vivo_local_bar, vivo_local_percentage, comp_local_vivo)


# —————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————

# [Global] Percentage of number of icons with the total of icons
# Define a helper function to calculate the global percentage
def calculate_global_percentage(name, num_icons, total_icons):
    return int((100 * num_icons) / total_icons)

# Calculate the global percentage for each set
telefonica_global_percentage = calculate_global_percentage("Telefónica", len_icons_telefonica, len_total_icons)
o2_global_percentage = calculate_global_percentage("O₂", len_icons_o2, len_total_icons)
blau_global_percentage = calculate_global_percentage("Blau", len_icons_blau, len_total_icons)
vivo_global_percentage = calculate_global_percentage("Vivo", len_icons_vivo, len_total_icons)

print(telefonica_global_percentage)

# Composition of GLOBAL (X / Y) for markdown
comp_global_telefonica, comp_global_o2, comp_global_blau, comp_global_vivo = [f" ({len_icons} / {len_total_icons})" for len_icons in [len_icons_telefonica, len_icons_o2, len_icons_blau, len_icons_vivo]]

# GLOBAL BARS
def generate_bars_and_percentage(len_icons, len_total_icons):
    percentage = int((100 * len_icons) / len_total_icons)
    bar = (int(percentage / 10) * 2) * BAR_FILLED_S + \
        BAR_EMPTY_S * (abs(int(percentage / 10) - 10) * 2)
    composition = " " + \
        "(" + str(len_icons) + " / " + str(len(total_icons)) + ")"
    return bar, percentage, composition

telefonica_global_bar, telefonica_global_percentage, comp_global_telefonica = generate_bars_and_percentage(len_icons_telefonica, len_total_icons)
o2_global_bar, o2_global_percentage, comp_global_o2 = generate_bars_and_percentage(len_icons_o2, len_total_icons)
blau_global_bar, blau_global_percentage, comp_global_blau = generate_bars_and_percentage(len_icons_blau, len_total_icons)
vivo_global_bar, vivo_global_percentage, comp_global_vivo = generate_bars_and_percentage(len_icons_vivo, len_total_icons)

# Composition of GLOBAL BAR + (X / Y) for markdown
def create_bar_string(percentage, comp_string):
    bar = (int(percentage / 10) * 2) * BAR_FILLED_S + \
        BAR_EMPTY_S * (abs(int(percentage / 10) - 10) * 2)
    return f"{bar}    {percentage}%{comp_string} `global`  "
    
telefonica_global = create_bar_string(telefonica_global_percentage, comp_global_telefonica)
o2_global = create_bar_string(o2_global_percentage, comp_global_o2)
blau_global = create_bar_string(blau_global_percentage, comp_global_blau)
vivo_global = create_bar_string(vivo_global_percentage, comp_global_vivo)

# —————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————

if __name__ == '__main__':
    path = sys.argv[1]
    brands = read_folder(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "![Mistica Icons](.github/resources/mistica-icons-light.svg#gh-light-mode-only)" + BREAK + "![Mistica Icons](.github/resources/mistica-icons-dark.svg#gh-dark-mode-only)" + BREAK + BREAK + "## What is this?  " + BREAK + BREAK + "This is the repo that contains all icons that is working in [Mistica Design](https://github.com/Telefonica/mistica-design) now.  " + BREAK + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10).  " + \
        BREAK + BREAK + "## Documentation" + BREAK + BREAK + "### Develop" + BREAK + BREAK + "#### iOS and Android" + BREAK + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + BREAK + "#### Web" + BREAK + BREAK + \
        "Visit [Mistica Storybook](https://mistica-web.vercel.app/?path=/story/icons-catalog--catalog) to get all the detail about using Mistica Icons Library" + BREAK + BREAK + "### Design" + BREAK + BREAK + "Use Mística icons library in Figma!" + BREAK + BREAK + \
        "## Icon equivalence status" + BREAK + BREAK + "**Local** = Icon equivalence in this set  " + BREAK + "**Global** = Icon set equivalence with total icons" + BREAK + BREAK + "---telefonica_local_BAR---" + BREAK + "---telefonica_global_BAR---" + BREAK + BREAK + "---o2_local_BAR---" + BREAK + "---o2_global_BAR---" + BREAK + BREAK + "---blau_local_BAR---" + BREAK + "---blau_global_BAR---" + BREAK + BREAK + "---vivo_local_BAR---" + BREAK + "---vivo_global_BAR---" + BREAK + BREAK + \
        "## Icons" + BREAK + BREAK + "| ---BRANDS--- | icon name |" + \
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
                # file_path_pdf = root + SLASH + brand + SLASH + style + SLASH + icon_name + PDF_EXTENSION
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
    file_content = file_content.replace(
        "---telefonica_global_BAR---", (telefonica_global))
    file_content = file_content.replace(
        "---telefonica_local_BAR---", (telefonica_local))
    file_content = file_content.replace("---o2_global_BAR---", (o2_global))
    file_content = file_content.replace(
        "---o2_local_BAR---", (o2_local))
    file_content = file_content.replace(
        "---blau_global_BAR---", (blau_global))
    file_content = file_content.replace(
        "---blau_local_BAR---", (blau_local))
    file_content = file_content.replace(
        "---vivo_global_BAR---", (vivo_global))
    file_content = file_content.replace(
        "---vivo_local_BAR---", (vivo_local))
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
            # row = "| telefonica | O2 | my_icon_light |
            row = PIPE + PIPE.join(icon_images) + PIPE + \
                "`" + icon_name + "`" + \
                "[" + "![" + icon_name + "]" + \
                "(.github/resources/anchor.svg)" + \
                "]" + "(" + "#" + icon_name + ")" + PIPE
            # + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")" + PIPE + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")"
            file_content += row + BREAK

    output_file_path = "./README.md"
    print(output_file_path)
    print(file_content)
    file = open(output_file_path, "w+")
    file.write(file_content)
    file.close()
