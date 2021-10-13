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


if __name__ == '__main__':
    path = sys.argv[1]
    brands = read_folder(path)
    root = os.path.basename(path)
    dictionary = {}
    file_content = "<br/><br/>![Mistica Icons](.github/resources/misticaicons-logo.png)<br/><br/>" + BREAK + "### What is this?" + BREAK + "This is the repo that contains all icons that is working in [Mistica Design](https://github.com/Telefonica/mistica-design) now." + BREAK + "Mistica support [Brand Factory icons](https://brandfactory.telefonica.com/document/1086#/nuestra-identidad/iconos). This set of icons are a big list of different icons and style that Brand Team worked to be used through Telefonica applications." + BREAK + "If you have any question, please you can ask directly in the app of Microsoft Teams, in [Mistica Team](https://teams.microsoft.com/l/team/19%3ad2e3607a32ec411b8bf492f43cd0fe0c%40thread.tacv2/conversations?groupId=e265fe99-929f-45d1-8154-699649674a40&tenantId=9744600e-3e04-492e-baa1-25ec245c6f10)." + BREAK + "### Documentation" + BREAK + "#### Develop" + BREAK + "##### iOS and Android" + BREAK + "You can get .pdf or .svg files from this repo." + BREAK + "##### Web" + BREAK + "Visit [Mistica Storybook](https://mistica-web.now.sh/?path=/story/icons-mistica-icons--catalog) to get all the detail about using Mistica Icons Library" + BREAK + "#### Design" + BREAK + "Install Mistica Icons Library in Sketch from [Mistica Manager](https://telefonica.github.io/mistica/docs/design/start-using)" + BREAK + "# Icons " + BREAK + "| ---BRANDS--- | icon name <img width=630> | " + BREAK + "| ---HEADER-BREAK--- |" + ":--- |" + BREAK
    for brand in brands:
        brand_folder = path + SLASH + brand
        styles = read_folder(brand_folder)
        for style in styles:
            style_folder = brand_folder + SLASH + style
            icons = read_folder(style_folder)
            for icon in icons:
                icon_name = os.path.splitext(icon)[0]
                file_path = root + SLASH + brand + SLASH + style + SLASH + icon_name + SVG_EXTENSION
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
    file_content = file_content.replace("---BRANDS---", separator.join(brands))
    file_content = file_content.replace("---HEADER-BREAK---", separator.join([":---:"] * (len(brands))))

    for icon_name in sorted(dictionary.keys()):
        icon = dictionary[icon_name]
        for style in sorted(icon.keys()):
            icon_images = []
            for brand in brands:
                icon_image = " ![" + icon_name + "](" + icon[style][brand] + ") " if brand in icon[style] else " "
                icon_images.append(icon_image)
            # row = "| default | O2 | my_icon_light |
            row = PIPE + PIPE.join(icon_images) + PIPE + "`" + icon_name + "`" + PIPE
            file_content += row + BREAK

    output_file_path = "./README.md"
    print(output_file_path)
    print(file_content)
    file = open(output_file_path, "w+")
    file.write(file_content)
    file.close()
