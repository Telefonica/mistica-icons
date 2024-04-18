import os

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

def generate_icon_table(path):  # Renombrar la función para que coincida con el nombre del módulo
    brands = [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]
    root = os.path.basename(path)
    dictionary = {}
    file_content = BREAK + "| ---BRANDS--- | icon name |" + \
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
            row = PIPE + PIPE.join(icon_images) + PIPE + \
                "<a id=" + "'" + icon_name + "'>"+ "`" + icon_name + "`"  + "</a>" + \
                "[" + "![" + icon_name + "]" + \
                "(.github/resources/anchor.svg)" + \
                "]" + "(" + "#" + icon_name + ")" + PIPE
            file_content += row + BREAK

    return file_content  # Devolver el contenido de la tabla de iconos
