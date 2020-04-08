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
    file_content = "# Esto es un H1" + BREAK + "## Esto es un H2" + BREAK + "### NO PUEDES USAR TILDES ni caracteres rarunos, dará fallo. (DO IT IN ENGLISH ANYWAY)" + BREAK + "[Y aqui tienes una guia de markdown link](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)" + BREAK +"| global | name | SVG | PDF | | O2 | name | SVG | PDF |" + BREAK + "| :-: | :- | :-: | :-: | - | :-: | :- | :-: | :-: |" + BREAK
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
