import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter
from sys import setrecursionlimit

with open("./10th/pipe_maze_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

UNKNOWN = 0
IS_ON_LOOP = 1
IS_ENCLOSED_BY_LOOP = 2
IS_NOT_ENCLOSED_BY_LOOP = 3

NETWORK = [[[pipe, UNKNOWN] for pipe in line] for line in lines]
STEP_DIRECTIONS = {(1, 0), (-1, 0), (0, 1), (0, -1)}

# ----------------------------------------- PART ONE: FIND LOOP ---------------------------------------
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

        if valid:
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

        NETWORK[row][col][1] = IS_ON_LOOP

        for direction in directions:
            next_position = (row + direction[0], col + direction[1])

            valid_next_directions, found_loop = try_all_directions(next_position, direction)
            new_next_directions += [(next_position, valid_next_directions)]

            if found_loop:
                found_loop_in = current_position
                NETWORK[next_position[0]][next_position[1]][1] = IS_ON_LOOP
                break
        
        if found_loop:
            break
    
    if len(new_next_directions) == 0:
        found_loop = True

    next_directions = new_next_directions



# --------------------------------------------- PART TWO: FIND ALL TILES OUTSIDE LOOP ---------------------------------------------------
# With all parts of the loop identified, time to find enclosed tiles

def adjacent_tiles(row, col):
    next_to_wall = row == 0 or col == 0 or row == len(NETWORK) - 1 or col == len(NETWORK[0]) - 1
    adj_tiles = []
    for step in STEP_DIRECTIONS:
        adj_row = row + step[0]
        adj_col = col + step[1]
        
        if adj_row >= 0 and adj_col >= 0 and adj_row < len(NETWORK) and adj_col < len(NETWORK[0]):
            tile = NETWORK[adj_row][adj_col]
            adj_tiles += [(tile, (adj_row, adj_col))]
    return adj_tiles, next_to_wall

def check_and_mark_tile_unenclosed(tile, row, col):
    if tile[1] != UNKNOWN:
        return
    adj_tiles, next_to_wall = adjacent_tiles(row, col)
    if next_to_wall:
        tile[1] = IS_NOT_ENCLOSED_BY_LOOP
    else:
        for adjacent_tile in adj_tiles:
            if adjacent_tile[0][1] == IS_NOT_ENCLOSED_BY_LOOP:
                tile[1] = IS_NOT_ENCLOSED_BY_LOOP
                break

def mark_tiles_next_to_unenclosed_as_unenclosed():
    for row, tiles in enumerate(NETWORK):
        for col, tile in enumerate(tiles):
                check_and_mark_tile_unenclosed(tile, row, col)

# First iteration: find all tiles directly connected to edges
upper_row_limit = len(NETWORK)
upper_col_limit = len(NETWORK[0])

for col in range(upper_col_limit):
    row = 0
    tile = NETWORK[row][col]
    check_and_mark_tile_unenclosed(tile, row, col)
for row in range(1, upper_row_limit- 1):
    col = 0
    tile = NETWORK[row][col]
    check_and_mark_tile_unenclosed(tile, row, col)
    col =upper_col_limit - 1
    tile = NETWORK[row][col]
    check_and_mark_tile_unenclosed(tile, row, col)
for col in range(upper_col_limit):
    row = upper_row_limit - 1
    tile = NETWORK[row][col]
    check_and_mark_tile_unenclosed(tile, row, col)

# try to cover everything
for i in range(len(NETWORK)):
    mark_tiles_next_to_unenclosed_as_unenclosed()
    


# ------------------------------------------- PART THREE: FIND ALL UNENCLOSED TILES SURROUNDED BY LOOP TILES --------------------------------------------------
# Find all unknown nodes on one side of loop tiles (here: left)

def left_if_dir_is(step):
    return (-step[1], step[0])

def right_if_dir_is(step):
    return (step[1], -step[0])

def adjacent_on_loop(row, col):
    adj_tiles, _ = adjacent_tiles(row, col)
    for tile in adj_tiles:
        if tile[0][1] == IS_ON_LOOP:
            return tile
    return None

def set_tiles_on_left_unenclosed(row, col, direction, next_direction):
    dirs = [direction, next_direction]
    for dir in dirs:
        left = left_if_dir_is(dir)
        left_tile_row = row + left[0]
        left_tile_col = col + left[1]
        if left_tile_row >= 0 and left_tile_row < len(NETWORK) and left_tile_col >= 0 and left_tile_col < len(NETWORK[0]):
            left_tile = NETWORK[left_tile_row][left_tile_col]
            if left_tile[1] == UNKNOWN:
                left_tile[1] = IS_NOT_ENCLOSED_BY_LOOP

tile_on_loop = None
direction = None
for row, tiles in enumerate(NETWORK):
    for col, tile in enumerate(tiles):
        if tile[1] == IS_NOT_ENCLOSED_BY_LOOP:
            tile_on_loop = adjacent_on_loop(row, col)
            if tile_on_loop is not None:
                (tile, (adj_row, adj_col)) = tile_on_loop
                direction = left_if_dir_is((adj_row - row, adj_col - col))
                break
    if tile_on_loop is not None:
        break

(tile, (row, col)) = tile_on_loop

(is_ok_dir, _) = valid_step(tile[0], direction, (row, col))
if not is_ok_dir:
    direction = right_if_dir_is(direction)

row += direction[0]
col += direction[1]
tile = NETWORK[row][col]
checked_tiles_on_loop = set({})

while (row, col) not in checked_tiles_on_loop:
    checked_tiles_on_loop.add((row, col))
    (directions, _) = try_all_directions((row, col), direction)
    # There should be only one valid direction
    next_direction = directions[0]
    set_tiles_on_left_unenclosed(row, col, direction, next_direction)
    direction = next_direction
    row += direction[0]
    col += direction[1]
    tile = NETWORK[row][col]

# one final time
(directions, _) = try_all_directions((row, col), direction)
next_direction = directions[0]
set_tiles_on_left_unenclosed(row, col, direction, next_direction)

# try to cover everything
for i in range(len(NETWORK)):
    mark_tiles_next_to_unenclosed_as_unenclosed()

result = 0

for row in NETWORK:
    for tile in row:
        if tile[1] == UNKNOWN:
            result += 1
            tile[1] = IS_ENCLOSED_BY_LOOP
print(result)