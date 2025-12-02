import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./11th/cosmic_expansion_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

SPACE = [list(line) for line in lines]

empty_row = ['!' for i in range(len(SPACE[0]))]

for i, line in enumerate(lines):
    if re.match(r"^\.+$", line):
        SPACE[i] = empty_row

for col in range(len(SPACE[0])):
    this_line = ""
    for row in range(len(SPACE)):
        this_line += SPACE[row][col]
    if re.match(r"^[.!]+$", this_line):
        for row in range(len(SPACE)):
            SPACE[row][col] = '!'

galaxy_coordinates = []
for r, row in enumerate(SPACE):
    for c, value in enumerate(row):
        if value == '#':
            galaxy_coordinates += [(r, c)]

result = 0
for i, coordinate in enumerate(galaxy_coordinates):
    for other_coordinate in galaxy_coordinates[i:]:

        diff = (abs(other_coordinate[0] - coordinate[0]), abs(other_coordinate[1] - coordinate[1]))
        empty_spaces_crossed = 0

        # Positive or negative direction
        if diff[0] != 0:
            iter_step_row = round((other_coordinate[0] - coordinate[0]) / diff[0])
        else:
            iter_step_row = 1

        if diff[1] != 0:
            iter_step_col = round((other_coordinate[1] - coordinate[1]) / diff[1])
        else:
            iter_step_col = 1            

        for row in range(coordinate[0], other_coordinate[0], iter_step_row):
            if SPACE[row][0] == '!':
                empty_spaces_crossed += 1

        for col in range(coordinate[1], other_coordinate[1], iter_step_col):
            if SPACE[0][col] == '!':
                empty_spaces_crossed += 1

        distance = diff[0] + diff[1] + empty_spaces_crossed * (1000000 - 1)

        #print(f"Total empty spaces crossed between {coordinate}, {other_coordinate}: {empty_spaces_crossed}")
        #print(f"for a total distance of {distance}")

        result += distance

print(result)