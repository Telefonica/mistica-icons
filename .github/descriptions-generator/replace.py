# Clonar el repo de mistica-icons en tu ordenador y asegurate de estar en production con la rama actualizada

# Asegurar que icons-keywords.json está actualizado y tiene la línea con el nombre del icono

# Abre el plugin de Figma Bulk Meta
# Exporta el json y llamalo telefonica-original.json, guárdalo en el repo en resources/descriptions-generator
# Correr el script en terminal “python3 replace.py” asegurándote que en el script está la información correcta. (debes cambiar los nombres de los archivos según el set de iconos que estás exportando, hay comentarios en las líneas que debes cambiar)

# Abre el plugin de Figma Bulk Meta
# Ir a la pestaña “Import” y seleccionar el archivo telefonica.json generado por el script

import json

# ————— CAMBIAR BRAND POR EL NOMBRE DE LA MARCA ————— #
brand = "telefonica"

# Construir la ruta del archivo utilizando la variable
ruta_original = f'./.github/descriptions-generator/originals/{brand}-original.json'
ruta_generated = f'./.github/descriptions-generator/generated/{brand}.json'

# Leer el JSON original desde el archivo
with open(ruta_original, 'r') as original_file:
    json_original = json.load(original_file)

# Leer el mapeo de palabras clave desde el archivo
# NO TOCAR #
with open('./icons/icons-keywords.json', 'r') as palabrasclave_file:
    palabras_clave = json.load(palabrasclave_file)

# Función para reemplazar la descripción
def reemplazar_descripcion(json, palabras_clave):
    nuevo_json = {}

    for clave, item in json.items():
        # Eliminar "light", "regular" y "filled" de la clave
        clave_sin_variantes = clave.replace('-light', '').replace('-regular', '').replace('-filled', '')

        if clave_sin_variantes in palabras_clave:
            palabras = palabras_clave[clave_sin_variantes]
            nueva_descripcion = ', '.join(palabras)
        else:
            nueva_descripcion = item["description"]

        # Copiar el objeto original y actualizar la descripción
        nuevo_item = item.copy()
        nuevo_item['description'] = nueva_descripcion
        nuevo_json[clave] = nuevo_item

    return nuevo_json

# Llamar a la función para obtener el nuevo JSON
json_actualizado = reemplazar_descripcion(json_original, palabras_clave)

# Escribir el JSON actualizado en un nuevo archivo
# ————— CAMBIAR BRAND POR EL NOMBRE DE LA MARCA ————— #
with open(ruta_generated, 'w') as nuevo_file:
    json.dump(json_actualizado, nuevo_file, indent=2)
