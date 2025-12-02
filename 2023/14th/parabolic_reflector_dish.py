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

def shift(col, index):
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

def shift_all_in_col(col):
    for i in reversed(range(len(col))):
        if col[i] == 'O':
            shift(col, i)

def calculate_load(col):
    load = 0
    for i in range(len(col)):
        if col[i] == 'O':
            load += i + 1
    return load

result = 0
for col in platform:
    shift_all_in_col(col)
    result += calculate_load(col)

print(result)