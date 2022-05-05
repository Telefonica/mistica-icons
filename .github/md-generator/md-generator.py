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


icons_telefonica = set()
icons_o2 = set()
icons_blau = set()

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

# print(len(icons_telefonica))
# print(len(icons_o2))
# print(len(icons_blau))
# print(len(total_icons))

total_icons = sorted(set.union(icons_telefonica, icons_o2, icons_blau))

BAR_FILLED = "<img src='https://i.imgur.com/8pLUSBF.png' />"
BAR_EMPTY = "<img src='https://i.imgur.com/BLjOoR0.png' />"

telefonica_percent = (100 * len(icons_telefonica)) / len(total_icons)
o2_percent = (100 * len(icons_o2)) / len(total_icons)
blau_percent = (100 * len(icons_blau)) / len(total_icons)

print(telefonica_percent)

telefonica_bar = ("Telefónica set" + "<br/>" + (int(telefonica_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(telefonica_percent / 10) - 10) * 2) + "    " + str(
    int(telefonica_percent))
    + "%" + "  ")

o2_bar = ("O2 set" + "<br/>" + (int(o2_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(o2_percent / 10) - 10) * 2) + "    " + str(
    int(o2_percent))
    + "%" + "  ")

blau_bar = ("Blau set" + "<br/>" + (int(blau_percent / 10) * 2) * BAR_FILLED + BAR_EMPTY * (abs(int(blau_percent / 10) - 10) * 2) + "    " + str(
    int(blau_percent))
    + "%" + "  ")


if __name__ == '__main__':
    path = sys.argv[1]
    brands = read_folder(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "<br/><br/>![Mistica Icons](.github/resources/misticaicons-logo.png)<br/><br/>" + "[![Analytics](https://ga-beacon.appspot.com/UA-136245358-1/mistica-icons)](https://github.com/Telefonica/mistica-icons)" + BREAK + "### What is this?" + BREAK + "This is the repo that contains all icons that is working in [Mistica Design](https://github.com/Telefonica/mistica-design) now." + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10)." + \
        BREAK + "### Documentation" + BREAK + "#### Develop" + BREAK + "##### iOS and Android" + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + "##### Web" + BREAK + \
        "Visit [Mistica Storybook](https://mistica-web.now.sh/?path=/story/icons-mistica-icons--catalog) to get all the detail about using Mistica Icons Library" + BREAK + "#### Design" + BREAK + "Use Mística icons library in Figma!" + BREAK + \
        "### Icon equivalence status" + BREAK + "---telefonica_BAR---" + BREAK + "---O2_BAR---" + BREAK + "---BLAU_BAR---" + BREAK + \
        "# Icons " + BREAK + "| ---BRANDS--- | icon name <img width=500> | " + \
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
        "---telefonica_BAR---", (telefonica_bar))
    file_content = file_content.replace("---O2_BAR---", (o2_bar))
    file_content = file_content.replace("---BLAU_BAR---", (blau_bar))
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
                "<a href='#" + icon_name + "'>" + "`" + icon_name  + "`" + "<span id='" + icon_name + "'></span>" +  "  " + "![anchor](.github/resources/anchor.svg)" + "</a>" + PIPE
            # + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")" + PIPE + "[<img src='.github/resources/svg.png'>]" + "(" + file_path + ")" + "[<img src='.github/resources/pdf.png'>]" + "(" + file_path_pdf + ")"
            file_content += row + BREAK

    output_file_path = "./README.md"
    print(output_file_path)
    print(file_content)
    file = open(output_file_path, "w+")
    file.write(file_content)
    file.close()
