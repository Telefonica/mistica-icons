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


def count_files(path):
    return len(os.listdir(path))


icons_default_light = count_files(r'icons/default/1.Light')
icons_default_regular = count_files(r'icons/default/2.Regular')
icons_default_filled = count_files(r'icons/default/3.Filled')
total_default = icons_default_light + icons_default_regular + icons_default_filled

icons_o2_light = count_files(r'icons/o2/1.Light')
icons_o2_regular = count_files(r'icons/o2/2.Regular')
icons_o2_filled = count_files(r'icons/o2/3.Filled')
total_o2 = icons_o2_light + icons_o2_regular + icons_o2_filled

icons_blau_light = 0
icons_blau_regular = 0
icons_blau_filled = 0
total_blau = icons_blau_light + icons_blau_regular + icons_blau_filled

# print(int(total_default))
# print(int(total_o2))
# print(icons_o2)

default_percent = 100
o2_percent = (int((total_o2 * 100) / total_default))
blau_percent = (int((total_blau * 100) / total_default))

BAR_FILLED = "<img src='https://i.imgur.com/8pLUSBF.png' />"
BAR_EMPTY = "<img src='https://i.imgur.com/BLjOoR0.png' />"

default_bar = ("`" + "default set‎‎‎" + "`" + "    " + (int(default_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (
            abs(int(default_percent / 10) - 10) * 2) + "    " + str(int(default_percent))
      + "%" + "  ")
o2_bar = ("`" + "o2 set‎‎‎" + "`" + "              " + (int(o2_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(o2_percent / 10) - 10) * 2) + "    " + str(
    int(o2_percent))
      + "%" + "  ")
blau_bar = ("`" + "blau set‎‎‎" + "`" + "          " + (int(blau_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(blau_percent / 10) - 10) * 2) + "    " + str(
    int(blau_percent))
      + "%" + "  ")

if __name__ == '__main__':
    path = sys.argv[1]
    brands = read_folder(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "<br/><br/>![Mistica Icons](.github/resources/misticaicons-logo.png)<br/><br/>" + BREAK + "### What is this?" + BREAK + "This is the repo that contains all icons that is working in [Mistica Design](https://github.com/Telefonica/mistica-design) now." + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10)." + BREAK + "### Documentation" + BREAK + "#### Develop" + BREAK + "##### iOS and Android" + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + "##### Web" + BREAK + "Visit [Mistica Storybook](https://mistica-web.now.sh/?path=/story/icons-mistica-icons--catalog) to get all the detail about using Mistica Icons Library" + BREAK + "#### Design" + BREAK + "Install Mistica Icons Library in Sketch from [Mistica Manager](https://telefonica.github.io/mistica/docs/design/start-using)" + BREAK + "### Icon set status" + BREAK + "---DEFAULT_BAR---" + BREAK + "---O2_BAR---" + BREAK + "---BLAU_BAR---" + BREAK + "# Icons " + BREAK + "| ---BRANDS--- | icon name <img width=596> | " + BREAK + "| ---HEADER-BREAK--- |" + ":--- |" + BREAK
    for brand in brands:
        brand_folder = path + SLASH + brand
        styles = read_folder(brand_folder)
        for style in styles:
            style_folder = brand_folder + SLASH + style
            icons = read_folder(style_folder)
            for icon in icons:
                icon_name = os.path.splitext(icon)[0]
                file_path = root + SLASH + brand + SLASH + style + SLASH + icon_name + SVG_EXTENSION
                file_path_pdf = root + SLASH + brand + SLASH + style + SLASH + icon_name + PDF_EXTENSION
                if icon_name in dictionary:
                    if style not in dictionary[icon_name]:
                        dictionary[icon_name][style] = {brand: file_path}
                    else:
                        dictionary[icon_name][style][brand] = file_path
                else:
                    dictionary[icon_name] = {
                        style: {brand: file_path}
                    }

    brands.remove("default")
    brands = ["default"] + sorted(brands)
    separator = " " + PIPE + " "
    file_content = file_content.replace("---DEFAULT_BAR---", (default_bar))
    file_content = file_content.replace("---O2_BAR---", (o2_bar))
    file_content = file_content.replace("---BLAU_BAR---", (blau_bar))
    file_content = file_content.replace("---BRANDS---", separator.join(brands))
    file_content = file_content.replace("---HEADER-BREAK---", separator.join([":---:"] * (len(brands) + 2)))
    

    for icon_name in sorted(dictionary.keys()):
        icon = dictionary[icon_name]
        for style in sorted(icon.keys()):
            icon_images = []
            for brand in brands:
                icon_image = " ![" + icon_name + "](" + icon[style][brand] + ") " if brand in icon[style] else " "
                icon_images.append(icon_image)
            # row = "| default | O2 | my_icon_light |
            row = PIPE + PIPE.join(icon_images) + PIPE + "`" + icon_name + "`" + PIPE + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")" + PIPE + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")"
            file_content += row + BREAK

    output_file_path = "./README.md"
    print(output_file_path)
    print(file_content)
    file = open(output_file_path, "w+")
    file.write(file_content)
    file.close()
