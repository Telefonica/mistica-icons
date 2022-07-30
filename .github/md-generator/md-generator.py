# !/usr/bin/python

import os
import sys

PIPE = "|"
SLASH = "/"
SVG_EXTENSION = ".svg"
PDF_EXTENSION = ".pdf"
BREAK = "\n"

BAR_FILLED = "![bar_filled](https://i.imgur.com/8pLUSBF.png)"
BAR_EMPTY = "![bar_empty](https://i.imgur.com/BLjOoR0.png)"


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

# Adding icons to each list
for root, dirs, files in os.walk('icons/telefonica/'):
    for file in files:
        if file.endswith(".svg"):
            icons_telefonica.add(file)

for root, dirs, files in os.walk('icons/o2/'):
    for file in files:
        if file.endswith(".svg"):
            icons_o2.add(file)

for root, dirs, files in os.walk('icons/blau/'):
    for file in files:
        if file.endswith(".svg"):
            icons_blau.add(file)

# Length of brand lists
len_icons_telefonica = len(icons_telefonica)
len_icons_o2 = len(icons_o2)
len_icons_blau = len(icons_blau)

# Union of all icons (no repeated!)
total_icons = sorted(set.union(icons_telefonica, icons_o2, icons_blau))

# Total icons in integer format
len_total_icons = len(total_icons)

# Intersections lists
telefonica_intersection = icons_telefonica.intersection(
    set.union(icons_blau, icons_o2))
o2_intersection = icons_o2.intersection(
    set.union(icons_blau, icons_telefonica))
blau_intersection = icons_blau.intersection(
    set.union(icons_telefonica, icons_o2))

# Intersections lists in integer format
len_telefonica_intersection = len(telefonica_intersection)
len_o2_intersection = len(o2_intersection)
len_blau_intersection = len(blau_intersection)

# —————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————

# # [Local] Try to know how many icons has equivalence to other brand
telefonica_local_equivalence = len(
    icons_telefonica.intersection(set.union(icons_o2, icons_blau)))
o2_local_equivalence = len(
    icons_o2.intersection(set.union(icons_telefonica, icons_blau)))
blau_local_equivalence = len(
    icons_blau.intersection(set.union(icons_telefonica, icons_o2)))


# [Local] Percentage of number of icons with the total of icons
telefonica_local_percentage = int((
    100 * telefonica_local_equivalence) / len_icons_telefonica)
o2_local_percentage = int((
    100 * o2_local_equivalence) / len_icons_o2)
blau_local_percentage = int((
    100 * blau_local_equivalence) / len_icons_blau)


# LOCAL BARS
telefonica_local_bar = (int(telefonica_local_percentage / 10) * 2) * BAR_FILLED + \
    BAR_EMPTY * (abs(int(telefonica_local_percentage / 10) - 10) * 2)
o2_local_bar = (int(o2_local_percentage / 10) * 2) * BAR_FILLED + \
    BAR_EMPTY * (abs(int(o2_local_percentage / 10) - 10) * 2)
blau_local_bar = (int(blau_local_percentage / 10) * 2) * BAR_FILLED + \
    BAR_EMPTY * (abs(int(blau_local_percentage / 10) - 10) * 2)

# Composition of LOCAL (X / Y) for markdown
comp_local_telefonica = " " + \
    "(" + str(telefonica_local_equivalence) + \
    " / " + str(len(icons_telefonica)) + ")"
comp_local_o2 = " " + \
    "(" + str(o2_local_equivalence) + \
    " / " + str(len(icons_o2)) + ")"
comp_local_blau = " " + \
    "(" + str(blau_local_equivalence) + \
    " / " + str(len(icons_blau)) + ")"

# Composition of LOCAL BAR + (X / Y) for markdown
telefonica_local = ("Telefónica set  " + BREAK + telefonica_local_bar + "    " +
                    str(telefonica_local_percentage) + "%" + comp_local_telefonica + " `local`" + "  ")
o2_local = ("O₂ set  " + BREAK + o2_local_bar + "    " +
            str(o2_local_percentage) + "%" + comp_local_o2 + " `local`" + "  ")
blau_local = ("Blau set  " + BREAK + blau_local_bar + "    " +
              str(blau_local_percentage) + "%" + comp_local_blau + " `local`" + "  ")

# —————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————

# [Global] Percentage of number of icons with the total of icons
telefonica_global_percentage = int((
    100 * len_icons_telefonica) / len_total_icons)
o2_global_percentage = int((
    100 * len_icons_o2) / len_total_icons)
blau_global_percentage = int((
    100 * len_icons_blau) / len_total_icons)


print(telefonica_global_percentage)

# Composition of GLOBAL (X / Y) for markdown
comp_global_telefonica = " " + \
    "(" + str(len_icons_telefonica) + " / " + str(len(total_icons)) + ")"
comp_global_o2 = " " + \
    "(" + str(len_icons_o2) + " / " + str(len(total_icons)) + ")"
comp_global_blau = " " + \
    "(" + str(len_icons_blau) + " / " + str(len(total_icons)) + ")"

# GLOBAL BARS
telefonica_global_bar = (int(telefonica_global_percentage / 10) * 2) * BAR_FILLED + \
    BAR_EMPTY * (abs(int(telefonica_global_percentage / 10) - 10) * 2)
o2_global_bar = (int(o2_global_percentage / 10) * 2) * BAR_FILLED + \
    BAR_EMPTY * (abs(int(o2_global_percentage / 10) - 10) * 2)
blau_global_bar = (int(blau_global_percentage / 10) * 2) * BAR_FILLED + \
    BAR_EMPTY * (abs(int(blau_global_percentage / 10) - 10) * 2)

# Composition of GLOBAL BAR + (X / Y) for markdown
telefonica_global = (telefonica_global_bar + "    " +
                     str(telefonica_global_percentage) + "%" + comp_global_telefonica + " `global`" + "  ")
o2_global = (o2_global_bar + "    " +
             str(o2_global_percentage) + "%" + comp_global_o2 + " `global`" + "  ")
blau_global = (blau_global_bar + "    " +
               str(blau_global_percentage) + "%" + comp_global_blau + " `global`" + "  ")


# —————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————

if __name__ == '__main__':
    path = sys.argv[1]
    brands = read_folder(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "# Mística Icons" + BREAK + BREAK + "![Mistica Icons](.github/resources/mistica-icons.svg)" + BREAK + BREAK + "## What is this?  " + BREAK + BREAK + "This is the repo that contains all icons that is working in [Mistica Design](https://github.com/Telefonica/mistica-design) now.  " + BREAK + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10).  " + \
        BREAK + BREAK + "### Documentation" + BREAK + BREAK + "#### Develop" + BREAK + BREAK + "##### iOS and Android" + BREAK + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + BREAK + "##### Web" + BREAK + BREAK + \
        "Visit [Mistica Storybook](https://mistica-web.now.sh/?path=/story/icons-mistica-icons--catalog) to get all the detail about using Mistica Icons Library" + BREAK + BREAK + "#### Design" + BREAK + BREAK + "Use Mística icons library in Figma!" + BREAK + BREAK + \
        "### Icon equivalence status" + BREAK + BREAK + "**Local** = Icon equivalence in this pack  " + BREAK + "**Global** = Icon pack equivalence with total icons" + BREAK + BREAK + "---telefonica_local_BAR---" + BREAK + "---telefonica_global_BAR---" + BREAK + BREAK + "---o2_local_BAR---" + BREAK + "---o2_global_BAR---" + BREAK + BREAK + "---blau_local_BAR---" + BREAK + "---blau_global_BAR---" + BREAK + BREAK + \
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
    brands = ["telefonica"] + sorted(brands)
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
