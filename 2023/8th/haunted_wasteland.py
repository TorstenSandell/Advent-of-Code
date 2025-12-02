import re
from math import sqrt, floor, ceil
from collections import Counter

with open("./8th/haunted_wasteland_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

instructions = list(lines[0].replace('L','0').replace('R', '1'))
network = {}

for line in lines[2:]:
    key, value = line.split(' = ')
    left, right = value.replace('(', '').replace(')', '').split(', ')
    network[key] = (left, right)

result = 0
found = False
key = 'AAA'
while not found:
    for instruction in instructions:
        result += 1
        key = network[key][int(instruction)]
        if key == 'ZZZ':
            found = True
            break

print(result)