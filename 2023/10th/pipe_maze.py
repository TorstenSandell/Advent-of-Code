import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./10th/pipe_maze_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

NETWORK = [[[pipe, 0] for pipe in line] for line in lines]
STEP_DIRECTIONS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

# Find S(tart)
start = None
for i, row in enumerate(NETWORK):
    for j, entry in enumerate(row):
        if entry[0] == 'S':
            start = (i, j)
            break
    if start is not None:
        break

def has_connection_north(pipe):
    return pipe == 'J' or pipe == '|' or pipe == 'L' or pipe == 'S'

def has_connection_south(pipe):
    return pipe == '|' or pipe == 'F' or pipe == '7' or pipe == 'S'

def has_connection_east(pipe):
    return pipe == '-' or pipe == 'F' or pipe == 'L' or pipe == 'S'

def has_connection_west(pipe):
    return pipe == '-' or pipe == 'J' or pipe == '7' or pipe == 'S'

def valid_step(pipe, step, current_pos):
    this_pos_valid = False
    next_pos_valid = False
    next_pos = (current_pos[0] + step[0], current_pos[1] + step[1])

    # do not step out of bounds
    if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] >= len(NETWORK) or next_pos[1] >= len(NETWORK[0]):
        return (False, False)
    
    next_pipe = NETWORK[next_pos[0]][next_pos[1]][0]

    # node has already been calculated and is not start
    already_calculated =  NETWORK[next_pos[0]][next_pos[1]][1] > 0

    if step == (1, 0):  # try go south
        this_pos_valid = has_connection_south(pipe)
        next_pos_valid = has_connection_north(next_pipe)
    elif step == (-1, 0):  # try go north
        this_pos_valid = has_connection_north(pipe)
        next_pos_valid = has_connection_south(next_pipe)
    elif step == (0, 1):  # try go east
        this_pos_valid = has_connection_east(pipe)
        next_pos_valid = has_connection_west(next_pipe)
    elif step == (0, -1):  # try go west
        this_pos_valid = has_connection_west(pipe)
        next_pos_valid = has_connection_east(next_pipe)
    return (this_pos_valid and next_pos_valid, already_calculated)

def try_all_directions(current_pos, last_direction = None):
    valid_directions = []
    pipe = NETWORK[current_pos[0]][current_pos[1]][0]
    directions = STEP_DIRECTIONS.copy()
    found_loop = False

    # Do not step backwards
    if last_direction is not None:
        directions.remove((-last_direction[0], -last_direction[1]))

    for step in directions:
        
        (valid, already_calculated) = valid_step(pipe, step, current_pos)
        if valid and already_calculated:
            found_loop = True

        if valid_step(pipe, step, current_pos)[0]:
            valid_directions += [step]

    return valid_directions, found_loop

found_loop = False
directions, _ = try_all_directions(start)
next_directions = [(start, directions)]
distance = 0
result = -1

while not found_loop:
    new_next_directions = []
    for (current_position, directions) in next_directions:
        row = current_position[0]
        col = current_position[1]

        NETWORK[row][col][1] = distance

        for direction in directions:
            next_position = (row + direction[0], col + direction[1])

            valid_next_directions, found_loop = try_all_directions(next_position, direction)
            new_next_directions += [(next_position, valid_next_directions)]

            if found_loop:
                found_loop_in = current_position
                NETWORK[next_position[0]][next_position[1]][1] = distance + 1
                break
        
        if found_loop:
            break
    
    if len(new_next_directions) == 0:
        found_loop = True

    next_directions = new_next_directions
    distance += 1
    if found_loop:
        result = distance


print(result)