# from simple_servo_control.py
switch_servo_map = {
    11: ('22-13', 'down'),
    56: ('22-13', 'up'),
    62: ('21-13', 'up'),
    1: ('21-13', 'down'),
    65: ('20-13','up' ),
    40: ('20-13', 'down'),
    19: ('13-13', 'up'),
    45: ('13-13', 'down'),
    22: ('12-13', 'up'),
    36: ('12-13', 'down'),
    32: ('11-13', 'up'),
    38: ('11-13', 'down'),
    24: ('10-13', 'up'),
    39: ('10-13', 'down'),
    57: ('22-20', 'up'),
    9:  ('22-20', 'down'),
    55: ('21-20', 'up'),
    16: ('21-20', 'down'),
    63: ('20-20', 'up'),
    46: ('20-20', 'down'),
    21: ('13-20', 'up'),
    13: ('13-20', 'down'),
    27: ('12-20', 'up'),
    0:  ('12-20', 'down'),
    34: ('10-20', 'up'),
    50: ('10-20', 'down'),
    53: ('21-21', 'up'),
    41: ('21-21', 'down'),
    26: ('13-21', 'up'),
    49: ('13-21', 'down'),
    20: ('11-20', 'up'),
    35: ('11-20', 'down'),
    59: ('20-22', 'up'),
    44: ('20-22', 'down'),
    25: ('13-22', 'up'),
    14: ('13-22', 'down'),
    28: ('12-22', 'up'),
    5:  ('12-22', 'down'),
    58: ('22-12', 'up'),
    8:  ('22-12', 'down'),
    66: ('20-12', 'up'),
    6:  ('20-12', 'down'),
    52: ('13-12', 'up'),
    47: ('13-13', 'down'),
    31: ('12-12', 'up'),
    4:  ('12-12', 'down'),
    30: ('11-12', 'up'),
    43: ('11-12', 'down'),
    18: ('10-12', 'up'),
    17: ('10-12', 'down'),
    51: ('21-11', 'up'),
    48: ('21-11', 'down'),
    54: ('20-11', 'up'),
    15: ('20-11', 'down'),
    64: ('13-11', 'up'),
    7:  ('13-11', 'down'),
    33: ('11-11', 'up'),
    3:  ('11-11', 'down'),
    60: ('20-10', 'up'),
    42: ('20-10', 'down'),
    61: ('13-10', 'up'),
    12: ('13-10', 'down'),
    23: ('12-10', 'up'),
    2:  ('12-10', 'down'),
}

reactor_height = 7
numbering_base = 4
numbering_start = numbering_base
numbering_digits = 2

def cell_type(x, y):
    """ Type of the specified cell """
    return default_layout[y][x]

def cell_name(x, y):
    """ Label of the specified cell """
    return "" + cell_row_name(y) + "-" + cell_column_name(x)

def cell_column_name(x):
    """ Label of the specified column """
    return baseN(numbering_start + x, numbering_base).zfill(numbering_digits)

def cell_row_name(y):
    """ Label of the specified row """
    return baseN(numbering_start + reactor_height - y - 1, numbering_base).zfill(numbering_digits)

# Converts number to specified base, from the internets: http://stackoverflow.com/questions/2267362/convert-integer-to-a-string-in-a-given-numeric-base-in-python
def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])


default_layout = [[' ', ' ', '*', '*', '*', ' ', ' '],
                  [' ', '*', '#', '*', '*', '*', ' '],
                  ['*', '*', '*', '*', '*', '#', '*'],
                  ['*', '*', '*', '*', '*', '*', '*'],
                  ['*', '#', '*', '*', '*', '*', '*'],
                  [' ', '*', '*', '*', '#', '*', ' '],
                  [' ', ' ', '*', '*', '*', ' ', ' ']] 


cell_name_map = {}
for x in range(len(default_layout)):
    for y in range(len(default_layout)):
        if cell_type(x,y) <> '*':
            continue
        #print "cell %d,%d has name %s" % (x,y,cell_name(x,y))
        cell_name_map[cell_name(x,y)] = [x,y]
        
switch_name_map = {}
for pin,info in switch_servo_map.items():
    if not switch_name_map.has_key(info[0]):
        switch_name_map[info[0]] = {}
    switch_name_map[info[0]][info[1]] = pin

#print switch_name_map

for name,coords in cell_name_map.items():
    if not switch_name_map.has_key(name):
        continue
    switches = switch_name_map[name]
    if switches.has_key('up'):
        print "        %d: [%d, %d, 1] # %s up" % (switches['up'], coords[0], coords[1], name)
    if switches.has_key('down'):
        print "        %d: [%d, %d, 0] # %s down" % (switches['down'], coords[0], coords[1], name)

        

