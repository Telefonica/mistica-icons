from os import walk

def get_filenames(path):
    return set(next(walk(path), (None, None, []))[2])

icons_telefonica_light = get_filenames(r'../../icons/telefonica/1.Light')
icons_telefonica_regular = get_filenames(r'../../icons/telefonica/2.Regular')
icons_telefonica_filled = get_filenames(r'../../icons/telefonica/3.Filled')

total_telefonica = len(set.union(icons_telefonica_light, icons_telefonica_regular, icons_telefonica_filled))

icons_o2_light = get_filenames(r'../../icons/o2/1.Light')
icons_o2_regular = get_filenames(r'../../icons/o2/2.Regular')
icons_o2_filled = get_filenames(r'../../icons/o2/3.Filled')

total_o2 = len(set.union(icons_o2_light, icons_o2_regular, icons_o2_filled))

icons_blau_light = get_filenames(r'../../icons/blau/1.Light')
icons_blau_regular = get_filenames(r'../../icons/blau/2.Regular')
icons_blau_filled = get_filenames(r'../../icons/blau/3.Filled')

total_blau = len(set.union(icons_blau_light, icons_blau_regular, icons_blau_filled))

total_icons = total_telefonica + total_o2 + total_blau

BAR_FILLED = "B"
BAR_EMPTY = "0"

print(total_icons)
print(total_telefonica)

telefonica_percent = (100 * total_telefonica) / total_icons
o2_percent = (total_o2 * 100) / total_telefonica
blau_percent = (int((total_blau * 100) / total_telefonica))

telefonica_bar = ("`" + "telefonica set" + "`"+ (telefonica_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(telefonica_percent / 10 - 10) * 2) + str(
    int(telefonica_percent))
      + " %" + "  ")

o2_bar = ("`" + "o2 set" + "`"+ (o2_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(o2_percent / 10 - 10) * 2) + str(
    int(o2_percent))
      + " %" + "  ")

print(telefonica_bar)
print(o2_bar)

print((100 * total_o2) / total_icons)
print((100 * total_blau) / total_icons)