import webcolors


rgb = webcolors.name_to_rgb("yellow")
print("\033[38;2;" + str(rgb.red) + ';' + str(rgb.green) + ';' + str(rgb.blue) + 'm', 'hicham')

