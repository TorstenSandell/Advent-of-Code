import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter


with open("./17th/clumsy_crucible_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

MOVE_RANGE = range(4, 11)
DIRECTIONS = set([(1, 0), (0, 1), (-1, 0), (0, -1)])
GRID = [[[int(loss), {dir: (float('inf')) for dir in DIRECTIONS}] for loss in line] for line in lines]
UNVISITED = set() #set([((x, y), (dir, amount_in_dir)) for amount_in_dir in MOVE_RANGE for dir in DIRECTIONS for y in range(len(GRID[0])) for x in range(len(GRID))])
VISITED = set()
for dir in DIRECTIONS:
    GRID[0][0][1][dir] = 0
    UNVISITED.add(((0,0),dir))
MAX_X = len(GRID) - 1
MAX_Y = len(GRID[0]) - 1
EXIT_COORDS = (MAX_X, MAX_Y)
number_vertices = (MAX_X + 1) * (MAX_Y + 1) * len(DIRECTIONS)
print(f"Time complexity V^2, with V = {number_vertices}, for a total of {number_vertices ** 2}")

def valid_node(node):
    (x, y), direction = node
    return x in range(0, MAX_X + 1) and y in range(0, MAX_Y + 1) and direction in DIRECTIONS 

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

def get_edge_cost(from_node, dir, steps):
    (fx, fy), _ = from_node
    edge_cost = 0
    dir_x, dir_y = dir
    for step in range(1, steps + 1):
        edge_cost += GRID[fx + dir_x * step][fy + dir_y * step][0]
    #print(f"from {from_node} in dir {dir} in {steps} steps, the cost is {edge_cost}")
    return edge_cost

def get_neighbors(node):
    (x, y), dir = node
    dir_x, dir_y = dir
    opposite_dir = (-dir_x, -dir_y)
    neighbors = set()
    for new_dir in DIRECTIONS:
        if new_dir != dir and new_dir != opposite_dir:
            for steps in MOVE_RANGE:
                new_dir_x, new_dir_y = new_dir
                nx, ny = x + new_dir_x * steps, y + new_dir_y * steps
                neighbor = ((nx, ny), new_dir)
                if valid_node(neighbor):
                    neighbors.add(neighbor)
    #print(f"from {node} (has {GRID[x][y][1][dir]}) got {neighbors}")
    return neighbors

def calculate_neighbors(node):
    neighbors = get_neighbors(node)
    (x, y), direction = node
    node_value = GRID[x][y][1][direction]

    for neighbor in neighbors:
        if neighbor in VISITED:
            continue
        (nx, ny), direction = neighbor
        steps = max(abs(nx-x), abs(ny-y))
        move_cost = get_edge_cost(node, direction, steps)
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