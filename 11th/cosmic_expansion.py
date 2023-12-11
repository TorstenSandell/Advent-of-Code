import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./11th/cosmic_expansion_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

SPACE = [list(line) for line in lines]

rows_to_expand = []
for i, line in enumerate(lines):
    if re.match(r"^\.+$", line):
        rows_to_expand += [i]

cols_to_expand = []
for col in range(len(SPACE[0])):
    this_line = ""
    for row in range(len(SPACE)):
        this_line += SPACE[row][col]
    if re.match(r"^\.+$", this_line):
        cols_to_expand += [col]

empty_row = ['.' for i in range(len(SPACE))]
for row in reversed(rows_to_expand):
    SPACE = SPACE[:row] + [empty_row] + SPACE[row:]

for col in reversed(cols_to_expand):
    for r, row in enumerate(SPACE.copy()):
        SPACE[r] = row[:col] + ['.'] + row[col:]

galaxy_coordinates = []
for r, row in enumerate(SPACE):
    for c, value in enumerate(row):
        if value == '#':
            galaxy_coordinates += [(r, c)]

result = 0
for i, coordinate in enumerate(galaxy_coordinates):
    for other_coordinate in galaxy_coordinates[i:]:
        diff = (abs(other_coordinate[0] - coordinate[0]), abs(other_coordinate[1] - coordinate[1]))
        distance = diff[0] + diff[1]
        result += distance

print(result)


#for line in SPACE:
    #print(''.join(line))