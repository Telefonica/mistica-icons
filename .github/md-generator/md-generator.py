# !/usr/bin/python

import os
import sys

PIPE = "|"
SLASH = "/"
SVG_EXTENSION = ".svg"
PDF_EXTENSION = ".pdf"
BREAK = "\n"


def read_folder(folder):
    if os.path.isdir(folder):
        files = os.listdir(folder)
        if ".DS_Store" in files:
            files.remove(".DS_Store")
        return files
    return []


# def count_files(path):
#     return len(os.listdir(path))

from os import walk

def get_filenames(path):
    return set(next(walk(path), (None, None, []))[2])

icons_telefonica_light = get_filenames(r'icons/telefonica/1.Light')
icons_telefonica_regular = get_filenames(r'icons/telefonica/2.Regular')
icons_telefonica_filled = get_filenames(r'icons/telefonica/3.Filled')

total_telefonica = len(set.union(icons_telefonica_light, icons_telefonica_regular, icons_telefonica_filled))

icons_o2_light = get_filenames(r'icons/o2/1.Light')
icons_o2_regular = get_filenames(r'icons/o2/2.Regular')
icons_o2_filled = get_filenames(r'icons/o2/3.Filled')

total_o2 = len(set.union(icons_o2_light, icons_o2_regular, icons_o2_filled))

icons_blau_light = get_filenames(r'icons/blau/1.Light')
icons_blau_regular = get_filenames(r'icons/blau/2.Regular')
icons_blau_filled = get_filenames(r'icons/blau/3.Filled')

total_blau = len(set.union(icons_blau_light, icons_blau_regular, icons_blau_filled))

total_icons = total_telefonica + total_o2 + total_blau

print(total_icons)
print(total_telefonica)

telefonica_percent = (100 * total_telefonica) / total_icons
o2_percent = (total_o2 * 100) / total_icons
blau_percent = (int((total_blau * 100) / total_icons))

BAR_FILLED = "<img src='https://i.imgur.com/8pLUSBF.png' />"
BAR_EMPTY = "<img src='https://i.imgur.com/BLjOoR0.png' />"

telefonica_bar = ("Telefónica set" + "<br/>" + (int(telefonica_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(telefonica_percent / 10) - 10) * 2) + "    " + str(
    int(telefonica_percent))
      + " %" + "  ")

o2_bar = ("O2 set" + "<br/>" + (int(o2_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(o2_percent / 10) - 10) * 2) + "    " + str(
    int(o2_percent))
      + " %" + "  ")

blau_bar = ("Blau set" + "<br/>" + (int(blau_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(blau_percent / 10) - 10) * 2) + "    " + str(
    int(blau_percent))
      + " %" + "  ")


if __name__ == '__main__':
    path = sys.argv[1]
    brands = read_folder(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "<br/><br/>![Mistica Icons](.github/resources/misticaicons-logo.png)<br/><br/>" + BREAK + "### What is this?" + BREAK + "This is the repo that contains all icons that is working in [Mistica Design](https://github.com/Telefonica/mistica-design) now." + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10)." + BREAK + "### Documentation" + BREAK + "#### Develop" + BREAK + "##### iOS and Android" + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + "##### Web" + BREAK + "Visit [Mistica Storybook](https://mistica-web.now.sh/?path=/story/icons-mistica-icons--catalog) to get all the detail about using Mistica Icons Library" + BREAK + "#### Design" + BREAK + "Install Mistica Icons Library in Sketch from [Mistica Manager](https://brandfactory.telefonica.com/document/1846#/get-started/start-to-design/mistica-manager)" + BREAK + "### Icon set status" + BREAK + "---telefonica_BAR---" + BREAK + "---O2_BAR---" + BREAK + "---BLAU_BAR---" + BREAK + "# Icons " + BREAK + "| ---BRANDS--- | icon name <img width=500> | " + BREAK + "| ---HEADER-BREAK--- |" + ":--- |" + BREAK
    for brand in brands:
        brand_folder = path + SLASH + brand
        styles = read_folder(brand_folder)
        for style in styles:
            style_folder = brand_folder + SLASH + style
            icons = read_folder(style_folder)
            for icon in icons:
                icon_name = os.path.splitext(icon)[0]
                file_path = root + SLASH + brand + SLASH + style + SLASH + icon_name + SVG_EXTENSION
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
    file_content = file_content.replace("---telefonica_BAR---", (telefonica_bar))
    file_content = file_content.replace("---O2_BAR---", (o2_bar))
    file_content = file_content.replace("---BLAU_BAR---", (blau_bar))
    file_content = file_content.replace("---BRANDS---", separator.join(brands))
    file_content = file_content.replace("---HEADER-BREAK---", separator.join([":---:"] * (len(brands)))) # add (len(brands) + 2) to add svg & pdf download
    

    for icon_name in sorted(dictionary.keys()):
        icon = dictionary[icon_name]
        for style in sorted(icon.keys()):
            icon_images = []
            for brand in brands:
                icon_image = " ![" + icon_name + "](" + icon[style][brand] + ") " if brand in icon[style] else " "
                icon_images.append(icon_image)
            # row = "| telefonica | O2 | my_icon_light |
            row = PIPE + PIPE.join(icon_images) + PIPE + "`" + icon_name + "`" + PIPE 
            # + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")" + PIPE + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")"
            file_content += row + BREAK

    output_file_path = "./README.md"
    print(output_file_path)
    print(file_content)
    file = open(output_file_path, "w+")
    file.write(file_content)
    file.close()
