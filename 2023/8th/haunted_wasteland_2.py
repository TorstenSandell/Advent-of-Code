import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./8th/haunted_wasteland_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

instructions = list(lines[0].replace('L','0').replace('R', '1'))
network = {}

for line in lines[2:]:
    key, value = line.split(' = ')
    left, right = value.replace('(', '').replace(')', '').split(', ')
    network[key] = (left, right)

keys = []
loop_info = []
for key in network:
    if re.match('[A-Z0-9]{2}A', key):
        keys += [key]
        # (iterations to reach loop, found a loop, iterations in loop, calculated entire loop)
        loop_info += [[0, False, 0, False]]

result = 0
found = False

while not found:
    for instruction in instructions:
        for i, (key, info) in enumerate(zip(keys.copy(), loop_info)):
            keys[i] = network[key][int(instruction)]
            if not info[1]:
                info[0] += 1
            elif not info[3]:
                info[2] += 1

        for key, info in zip(keys, loop_info):
            if re.match('[A-Z0-9]{2}Z', key):
                if not info[1]:
                    info[1] = True
                elif not info[3]:
                    info[3] = True
                    info[0] = info[0] - info[2]

        found = True
        for info in loop_info:
            if not info[3]:
                found = False

# Following only works if info[0] == 0 for all info in loop_info
# This is true for my input

result = 1
for info in loop_info:
    iterations_in_loop = info[2]
    current_gcd = gcd(iterations_in_loop, result)
    result *= iterations_in_loop // current_gcd

print(result)
