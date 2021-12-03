from os import walk

def get_filenames(path):
    return set(next(walk(path), (None, None, []))[2])

icons_telefonica_light = get_filenames(r'../../icons/telefonica/1.Light')
icons_telefonica_regular = get_filenames(r'../../icons/telefonica/2.Regular')
icons_telefonica_filled = get_filenames(r'../../icons/telefonica/3.Filled')

total_telefonica = set.union(icons_telefonica_light, icons_telefonica_regular, icons_telefonica_filled)

print(total_telefonica)


icons_o2_light = get_filenames(r'../../icons/o2/1.Light')
icons_o2_regular = get_filenames(r'../../icons/o2/2.Regular')
icons_o2_filled = get_filenames(r'../../icons/o2/3.Filled')

total_o2 = set.union(icons_o2_light, icons_o2_regular, icons_o2_filled)

print(total_o2)

total_icons = set.union(total_telefonica, total_o2)

print(total_icons)
# no_ext = [s.replace(".pdf", "") for s in filenames]


import os

# for root, dirs, files in os.walk("../../icons/telefonica/"):
#   for file in files:
 #       if file.endswith(".svg"):
 #            print(os.path.join(root, file))

