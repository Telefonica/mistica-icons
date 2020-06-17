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
    file_content = '<div align="center"><img height="80" alt="Mística Logo" src="_resources/misticaicons_logo.svg"></div>' + BREAK + "### What is this?" + BREAK + "This is the repo that contains all icons that is working in [Mistica Design Libraries](https://github.com/Telefonica/mistica-design-libraries) now." + BREAK + "The icons that there is here are **the only source of true** from the design team in icons." + BREAK + "If you have any question, please you can ask directly in the Slack channel [#designsystem](https://tuentitu.slack.com/archives/CH3B76BDW)" + BREAK + "### Documentation" + BREAK + "You can find more information and how to use this repo in the [Wiki](https://github.com/Telefonica/mistica-icons/wiki)." + BREAK + "### Search in the repo" + BREAK + "The best way to search in this repo is using your browser's search engine (CMD + F):" + BREAK + "![Image of search engine](https://github.com/Telefonica/mistica-icons/blob/production/_resources/_imgs_github/github_img_1.png?raw=true)" + BREAK + "# Icons " + BREAK + "| global | name | SVG | PDF | | O2 | name | SVG | PDF |" + BREAK + "| :-: | :- | :-: | :-: | - | :-: | :- | :-: | :-: |" + BREAK
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

    for icon in dictionary:
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
