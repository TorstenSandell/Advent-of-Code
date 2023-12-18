import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter


with open("./17th/clumsy_crucible_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

# cost, min, entered from direction
DIRECTIONS = set([(1, 0), (0, 1), (-1, 0), (0, -1)])
GRID = [[[int(loss), {(dir, amount_in_dir): (float('inf')) for amount_in_dir in range(1, 4) for dir in DIRECTIONS}] for loss in line] for line in lines]
UNVISITED = set() #set([((x, y), (dir, amount_in_dir)) for amount_in_dir in range(1, 4) for dir in DIRECTIONS for y in range(len(GRID[0])) for x in range(len(GRID))])
VISITED = set()
for dir in DIRECTIONS:
    GRID[0][0][1][(dir, 1)] = 0
    UNVISITED.add(((0,0),(dir,1)))
MAX_X = len(GRID) - 1
MAX_Y = len(GRID[0]) - 1
EXIT_COORDS = (MAX_X, MAX_Y)
number_vertices = (MAX_X + 1) * (MAX_Y + 1) * 4 * len(DIRECTIONS)
print(f"Time complexity V^2, with V = {number_vertices}, for a total of {number_vertices ** 2}")

def valid_node(node):
    (x, y), (direction, amount_in_direction) = node
    return x in range(0, MAX_X + 1) and y in range(0, MAX_Y + 1) and direction in DIRECTIONS and amount_in_direction in range(1, 4)

def find_lowest_unvisited_node():
    lowest_node = None
    lowest_value = float('inf')
    for node in UNVISITED:
        (x, y), direction = node
        value = GRID[x][y][1][direction]
        if value < lowest_value:
            lowest_value = value
            lowest_node = node
    #print(f"found {lowest_node}: {lowest_value}")
    return lowest_node

def get_neighbors(node):
    (x, y), (dir, amount_in_dir) = node
    dir_x, dir_y = dir
    opposite_dir = (-dir_x, -dir_y)
    neighbors = set()
    nx, ny = x + dir_x, y + dir_y
    same_dir_neighbor = ((nx, ny), (dir, amount_in_dir + 1))
    if valid_node(same_dir_neighbor):
        neighbors.add(same_dir_neighbor)
    for new_dir in DIRECTIONS:
        if new_dir != dir and new_dir != opposite_dir:
            new_dir_x, new_dir_y = new_dir
            nx, ny = x + new_dir_x, y + new_dir_y
            neighbor = ((nx, ny), (new_dir, 1))
            if valid_node(neighbor):
                neighbors.add(neighbor)
    #print(f"from {node} got {neighbors}")
    return neighbors

def calculate_neighbors(node):
    neighbors = get_neighbors(node)
    (x, y), direction = node
    node_value = GRID[x][y][1][direction]

    for neighbor in neighbors:
        if neighbor in VISITED:
            continue
        (nx, ny), direction = neighbor
        move_cost = GRID[nx][ny][0]
        neighbor_value = GRID[nx][ny][1][direction]
        new_neighbor_value = move_cost + node_value

        if new_neighbor_value < neighbor_value:
            GRID[nx][ny][1][direction] = new_neighbor_value
            #print(f"set new value {new_neighbor_value} for {neighbor}")
            UNVISITED.add(neighbor)
    VISITED.add(node)
    UNVISITED.discard(node)
    

current_node = find_lowest_unvisited_node()
while current_node[0] != EXIT_COORDS:
    #print(f"got {current_node}")
    calculate_neighbors(current_node)
    current_node = find_lowest_unvisited_node()

#for row in GRID:
#    r = ''
#    for entry in row:
#        r += f"[{entry[0]}, {min(entry[1].values())}] "
#    print(r)

result = min(GRID[MAX_X][MAX_Y][1].values())
print(result)