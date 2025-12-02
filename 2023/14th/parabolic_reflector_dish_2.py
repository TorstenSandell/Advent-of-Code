import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./14th/parabolic_reflector_dish_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

platform = []
for col in range(len(lines[0])):
    platform += [[]]
    for row in range(len(lines)):
        platform[col] += [lines[row][col]]
    platform[col] = list(reversed(platform[col]))

original_platform = [col.copy() for col in platform]
goal_num_iterations = 1000000000

def shift_north(col, index):
    if col[index] != 'O':
        raise f"Wrong type of thing to shift: {col[index]} at {index} in {col}"
    if index + 1 >= len(col):
        return
    for i, value in enumerate(col[index+1:]):
        working_index = i + index + 1
        if value == 'O' or value == '#':
            col[index] = '.'
            col[working_index - 1] = 'O'
            break
        elif working_index == len(col) - 1:  # move to last
            col[index] = '.'
            col[working_index] = 'O'
            break

def shift_all_north(col):
    for i in reversed(range(len(col))):
        if col[i] == 'O':
            shift_north(col, i)

def calculate_load(col):
    load = 0
    for i in range(len(col)):
        if col[i] == 'O':
            load += i + 1
    return load

# Instead of shifting in other direction, rotate platform and shift in same direction
def rotate_90_degrees(platform):
    new_platform = [['' for j in range(len(platform))] for i in range(len(platform[0]))]
    for col, column in enumerate(list(reversed(platform))):
        for row, value in enumerate(column):
            new_platform[row][col] = value

    return new_platform

last_east_shift = platform
all_east_shifts = []
index_of_start_of_loop = -1

for i in range(goal_num_iterations):
    for j in range(4):
        for col in platform:
            shift_all_north(col)
        platform = rotate_90_degrees(platform)
    east_shift = [col.copy() for col in platform]
    if east_shift in all_east_shifts:
        index_of_start_of_loop = all_east_shifts.index(east_shift)
        break
    all_east_shifts += [[col.copy() for col in east_shift]]

length_of_loop = len(all_east_shifts) - index_of_start_of_loop
print(index_of_start_of_loop, length_of_loop)

num_iterations_equivalent_to_goal = index_of_start_of_loop + (goal_num_iterations - index_of_start_of_loop) % length_of_loop

platform = original_platform
for i in range(num_iterations_equivalent_to_goal):
    for i in range(4):
        for col in platform:
            shift_all_north(col)
        platform = rotate_90_degrees(platform)
    

result = 0

for col in platform:
    result += calculate_load(col)

print(result)