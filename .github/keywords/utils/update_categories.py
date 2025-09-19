import json
import re

# Crea un archivo de icons-categories.txt para categorizar iconos siguiendo esta estructura:
# iconName (category)
# Sin -regular / -light / -filled
# Ejemplo:
# arrow-down (Arrows)
# El script actualizará el campo "category" en icons-keywords.json
# para cada iconName encontrado en icons-categories.txt

# Paths
KEYWORDS_PATH = 'icons/icons-keywords.json'
CATEGORIES_PATH = 'icons/icons-categories.txt'
OUTPUT_PATH = 'icons/icons-keywords.json'

# Load icons-keywords
with open(KEYWORDS_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Read iconName (category) lines
def parse_icon_category(line):
    match = re.match(r'^(.*?)\s*\((.*?)\)\s*$', line)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return None, None

with open(CATEGORIES_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        icon, category = parse_icon_category(line)
        if icon and category and icon in data:
            data[icon]['category'] = [category]

# Save result
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'Categorías actualizadas en {OUTPUT_PATH}')
