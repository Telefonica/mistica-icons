# -*- coding: utf-8 -*-
import os

#
# def get_filenames(path):
#     for root, dirs, files in os.walk(path):
#         for file in files:
#             if file.endswith(".svg"):
#                 append(file)

icons_telefonica = set()
icons_o2 = set()
icons_blau = set()

for root, dirs, files in os.walk('../../icons/telefonica/'):
    for file in files:
        if file.endswith(".svg"):
            icons_telefonica.add(file)

for root, dirs, files in os.walk('../../icons/o2/'):
    for file in files:
        if file.endswith(".svg"):
            icons_o2.add(file)

for root, dirs, files in os.walk('../../icons/blau/'):
    for file in files:
        if file.endswith(".svg"):
            icons_blau.add(file)

print(len(icons_telefonica))
print(len(icons_o2))
print(len(icons_blau))

total_icons = sorted(set.union(icons_telefonica, icons_o2, icons_blau))

print(len(total_icons))
# print(len(sorted(set(icons_telefonica).intersection(total_icons))))
# print(len(sorted(set(icons_o2).intersection(total_icons))))
# print(len(sorted(set(icons_blau).intersection(total_icons))))

BAR_FILLED = "█"
BAR_EMPTY = "░"

telefonica_percent = (100 * len(icons_telefonica)) / len(total_icons)
o2_percent = (100 * len(icons_o2)) / len(total_icons)
blau_percent = (100 * len(icons_blau)) / len(total_icons)

telefonica_bar = ("`" + "telefonica set" + "`" + (telefonica_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(telefonica_percent / 10 - 10) * 2) + str(
    int(telefonica_percent))
      + " %" + "  ")

o2_bar = ("`" + "o2 set" + "`" + (o2_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(o2_percent / 10 - 10) * 2) + str(
    int(o2_percent))
      + " %" + "  ")

blau_bar = ("`" + "blau set" + "`" + (blau_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(blau_percent / 10 - 10) * 2) + str(
    int(blau_percent))
      + " %" + "  ")

print(telefonica_bar)
print(o2_bar)
print(blau_bar)


#
# # total_telefonica = len(set.union(icons_telefonica_light, icons_telefonica_regular, icons_telefonica_filled))
#
# icons_o2_light = get_filenames(r'../../icons/o2/1.Light')
# icons_o2_regular = get_filenames(r'../../icons/o2/2.Regular')
# icons_o2_filled = get_filenames(r'../../icons/o2/3.Filled')
#
# # total_o2 = len(set.union(icons_o2_light, icons_o2_regular, icons_o2_filled))
#
# icons_blau_light = get_filenames(r'../../icons/blau/1.Light')
# icons_blau_regular = get_filenames(r'../../icons/blau/2.Regular')
# icons_blau_filled = get_filenames(r'../../icons/blau/3.Filled')
#
# # total_blau = len(set.union(icons_blau_light, icons_blau_regular, icons_blau_filled))
#
# # total_icons = total_telefonica + total_o2 + total_blau
#
# BAR_FILLED = "█"
# BAR_EMPTY = "░"
#
# # print(total_icons)
# # print(total_telefonica)
#
# telefonica_percent = (100 * total_telefonica) / total_icons
# o2_percent = (total_o2 * 100) / total_telefonica
# blau_percent = (int((total_blau * 100) / total_telefonica))
#
# telefonica_bar = ("`" + "telefonica set" + "`"+ (telefonica_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(telefonica_percent / 10 - 10) * 2) + str(
#     int(telefonica_percent))
#       + " %" + "  ")
#
# o2_bar = ("`" + "o2 set" + "`"+ (o2_percent / 10 * 2) * BAR_FILLED + BAR_EMPTY * (abs(o2_percent / 10 - 10) * 2) + str(
#     int(o2_percent))
#       + " %" + "  ")
#
# # print(telefonica_bar)
# # print(o2_bar)
#
# # print((100 * total_o2) / total_icons)
# # print((100 * total_blau) / total_icons)