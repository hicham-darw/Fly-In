import re 


hub = "hub: waypoint1 1 0 [somthing]"
nb = "nb_drones: 2"


mtch = re.match("^hub: [a-zA-Z0-9]+ \d+ \d+( \[.+\])?", hub)
print(mtch.group());
