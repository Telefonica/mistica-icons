# !/usr/bin/python

import os
import sys

PIPE = "|"
SLASH = "/"
PNG_FOLDER = "PNG"
SVG_FOLDER = "SVG"
PDF_FOLDER = "PDF"
PNG_EXTENSION = ".png"
SVG_EXTENSION = ".svg"
PDF_EXTENSION = ".pdf"
BREAK = "\n"

if __name__ == '__main__':
    path = sys.argv[1]
    files = os.listdir(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "<br/><br/>![Mistica Icons](.github/resources/misticaicons-logo.png)<br/><br/>" + BREAK + "### What is this?" + BREAK + "This is the repo that contains all icons that is working in [Mistica Design Libraries](https://github.com/Telefonica/mistica-design-libraries) now." + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10)." + BREAK + "### Documentation" + BREAK + "#### Develop" + BREAK + "##### iOS and Android" + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + "##### Web" + BREAK + "Visit [Mistica Playroom](https://mistica-web.now.sh/?path=/story/icons-mistica-icons--catalog) to get all the detail about using Mistica Icons Library" + BREAK + "#### Design" + BREAK + "Install Mistica Icons Library in Sketch from [Mistica Manager](https://telefonica.github.io/mistica/docs/design/start-using)" + BREAK + "You can find more information and how to use this repo in the [Wiki](#). WIP" + BREAK + "### Search in the repo" + BREAK + "The best way to search in this repo is using your browser's search engine (CMD + F):" + BREAK + "![Image of search engine](.github/resources/imgs-github/github-img-1.png)" + BREAK + "# Icons " + BREAK + "| Icon | name | SVG | PDF |" + BREAK + "| :-: | :- | :-: | :-: |" + BREAK
    for brand in files:
        brand_folder = path + SLASH + brand
        if os.path.isdir(brand_folder) and brand != ".DS_Store":
            for icon in os.listdir(brand_folder):
                if icon != ".DS_Store":
                    icon_name = os.path.splitext(icon)[0]
                    icon_extension = os.path.splitext(icon)[1]
                    if icon_name in dictionary:
                        brands = dictionary[icon_name]
                        if brand not in brands:
                            brands.append(brand)
                    else:
                        dictionary[icon_name] = [brand]

    for icon in sorted(dictionary.keys()):
        line_image = PIPE
        line_separator = BREAK + PIPE
        line_name = BREAK + PIPE
        row = ""
        counter = 0
        dictionary[icon].sort()
        for brand in dictionary[icon]:
            path_icon = root + SLASH + brand + SLASH + icon + SVG_EXTENSION
            svg_icon = root + SLASH + brand + SLASH + icon + SVG_EXTENSION
            pdf_icon = root + SLASH + brand + SLASH + icon + PDF_EXTENSION
            row = row + "| ![" + icon + "](" + path_icon + ") | `" + icon + "`  |  [.svg](" + svg_icon + ") | [.pdf](" + pdf_icon + ") |  "
        file_content += row + BREAK

    output_file_path = "./README.md"
    print(output_file_path)
    print(file_content)
    file = open(output_file_path, "w+")
    file.write(file_content)
    file.close()
    