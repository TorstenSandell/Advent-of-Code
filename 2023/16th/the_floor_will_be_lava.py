import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./16th/the_floor_will_be_lava_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

GRID = [[None for j in range(len(lines[0]))] for i in range(len(lines))]

for i, line in enumerate(lines):
    for j, value in enumerate(line):
        # Energized, directions entered from
        GRID[i][j] = [value, False, set({})]

def next_directions(current_direction, x, y):
    value = GRID[x][y][0]
    if value == '.' or \
        (current_direction == (0, 1) or current_direction == (0, -1)) and value == '-' or \
        (current_direction == (1, 0) or current_direction == (-1, 0)) and value == '|':
        return set({current_direction})
    
    if (current_direction == (0, 1) or current_direction == (0, -1)) and value == '|':
        return set({(1, 0), (-1, 0)})
    
    if (current_direction == (1, 0) or current_direction == (-1, 0)) and value == '-':
        return set({(0, 1), (0, -1)})
    
    if  current_direction == (0, 1) and value == '/' or \
        current_direction == (0, -1) and value == '\\':
        return set({(-1, 0)})
    
    if  current_direction == (0, -1) and value == '/' or \
        current_direction == (0, 1) and value == '\\':
        return set({(1, 0)})
    
    if  current_direction == (1, 0) and value == '/' or \
        current_direction == (-1, 0) and value == '\\':
        return set({(0, -1)})
    
    if  current_direction == (-1, 0) and value == '/' or \
        current_direction == (1, 0) and value == '\\':
        return set({(0, 1)})
    
steps_to_take = set({((0, 1), 0, 0)})

while len(steps_to_take) > 0:
    current_direction, x, y = steps_to_take.pop()
    GRID[x][y][1] = True
    GRID[x][y][2].add(current_direction)
    next_dirs = next_directions(current_direction, x, y)
    #print(current_direction, x, y, GRID[x][y][0], next_dirs)
    for next_direction in next_dirs:
        next_x = x + next_direction[0]
        next_y = y + next_direction[1]
        if next_x < len(GRID) and next_y < len(GRID[next_x]) and 0 <= next_x and 0<= next_y and \
            next_direction not in GRID[next_x][next_y][2]:
            steps_to_take.add((next_direction, next_x, next_y))

result = 0
for i in range(len(GRID)):
    #line = ''
    for j in range(len(GRID[i])):
        #next_value = '.'
        if GRID[i][j][1]:
            result += 1
            #next_value = '#'
        #line += next_value
    #print(line)

print(result)