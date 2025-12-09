import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter


with open("./18th/lavaduct_lagoon_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

direction_map = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

instructions = []
for line in lines:
    direction, steps, color = line.split(" ")
    instructions += [(direction_map[direction], int(steps), color)]

current_coordinate = (0,0)
filled_coordinates = set()
filled_coordinates.add(current_coordinate)

for instruction in instructions:
    direction, steps, _ = instruction
    dir_x, dir_y = direction
    for step in range(1, steps + 1):
        x, y = current_coordinate
        current_coordinate = (x + dir_x, y + dir_y)
        filled_coordinates.add(current_coordinate)

min_x = float('inf')
min_y = float('inf')
max_x = - float('inf')
max_y = - float('inf')
for coordinate in filled_coordinates:
    x, y = coordinate
    if x < min_x:
        min_x = x
    if y < min_y:
        min_y = y
    if x > max_x:
        max_x = x
    if y > max_y:
        max_y = y

X_RANGE = range(min_x, max_x + 1)
Y_RANGE = range(min_y, max_y + 1)

GRID = [['.' for y in Y_RANGE] for x in X_RANGE]

for coordinate in filled_coordinates:
    x, y = coordinate
    adj_x, adj_y = x - min_x, y - min_y
    GRID[adj_x][adj_y] = '#'

OUTSIDE = set()

def get_neighboring_non_filled_coords(x, y):
    non_filled_coords = set()
    for xx in range(x - 1, x + 2):
        for yy in range(y - 1, y + 2):
            if 0 <= xx < len(GRID) and 0 <= yy < len(GRID[0]) and \
                GRID[xx][yy] == '.':
                    non_filled_coords.add((xx,yy))
    return non_filled_coords
                

def mark_outsides():
    outside_coords = set()
    for x in range(len(GRID)):
        if GRID[x][0] == '.':
            outside_coords.add((x,0))
        if GRID[x][len(GRID[0]) - 1] == '.':
            outside_coords.add((x,len(GRID[0]) - 1))
    for y in range(len(GRID[0])):
        if GRID[0][y] == '.':
            outside_coords.add((0,y))
        if GRID[len(GRID) - 1][y] == '.':
            outside_coords.add((len(GRID) - 1, y))
    while len(outside_coords) != 0:
        (x, y) = outside_coords.pop()
        GRID[x][y] = 'x'
        outside_coords = outside_coords.union(get_neighboring_non_filled_coords(x,y))

def mark_unmarked_as_filled():
    for row in GRID:
        for i in range(len(row)):
            if row[i] == '.':
                row[i] = '#'


def get_amount_filled():
    r = 0
    for row in GRID:
        for value in row:
            if value == '#':
                r += 1
    return r


mark_outsides()
mark_unmarked_as_filled()
result = get_amount_filled()


for row in GRID:
    str = ''
    for char in row:
        str += char
    print(str)
print(result)
