import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter


with open("./18th/lavaduct_lagoon_example_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

number_to_direction = ['R', 'D', 'L', 'U']
direction_map = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}

instructions = []
for line in lines:
    instruction = re.sub(r'[()#]', '', line.split(" ")[-1])
    direction = direction_map[number_to_direction[int(instruction[-1])]]
    steps = int(instruction[:5], 16)
    inst = (direction, steps)
    instructions += [inst]
    print(inst)



