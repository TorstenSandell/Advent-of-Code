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

def next_directions(current_direction, x, y, grid):
    value = grid[x][y][0]
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
    
def reflect_light(start_dir, start_x, start_y):
    grid = [[[entry[0], entry[1], entry[2].copy()] for entry in GRID[row]] for row in range(len(GRID))]
    '''
    for i in range(len(grid)):
        line = ''
        for j in range(len(grid[i])):
            line += grid[i][j][0]
        print(line)
    print()
    '''
    steps_to_take = set({(start_dir, start_x, start_y)})
    while len(steps_to_take) > 0:
        current_direction, x, y = steps_to_take.pop()
        grid[x][y][1] = True
        grid[x][y][2].add(current_direction)
        next_dirs = next_directions(current_direction, x, y, grid)
        #print(current_direction, x, y, GRID[x][y][0], next_dirs)
        for next_direction in next_dirs:
            next_x = x + next_direction[0]
            next_y = y + next_direction[1]
            if next_x < len(grid) and next_y < len(grid[next_x]) and 0 <= next_x and 0<= next_y and \
                next_direction not in grid[next_x][next_y][2]:
                steps_to_take.add((next_direction, next_x, next_y))

    result = 0
    for i in range(len(grid)):
        #line = ''
        for j in range(len(grid[i])):
            #next_value = '.'
            if grid[i][j][1]:
                result += 1
                #next_value = '#'
            #line += next_value
        #print(line)
    #print()
    return result

result = 0
for row in range(len(GRID)):
    #print(f"starting from {row}, 0 in direction (0, 1)")
    new_result = reflect_light((0, 1), row, 0)
    result = max(result, new_result)

    #print(f"starting from {row}, {len(GRID[row]) - 1} in direction (0, -1)")
    new_result = reflect_light((0, -1), row, len(GRID[row]) - 1)
    result = max(result, new_result)

for col in range(len(GRID[0])):
    #print(f"starting from 0, {col} in direction (1, 0)")
    new_result = reflect_light((1, 0), 0, col)
    result = max(result, new_result)
    
    #print(f"starting from {len(GRID) - 1}, {col} in direction (-1, 0)")
    new_result = reflect_light((-1, 0), len(GRID) - 1, col)
    result = max(result, new_result)

print(result)