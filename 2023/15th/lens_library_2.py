import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./15th/lens_library_input.txt", mode='r', encoding='utf-8') as input:
    line = input.read().splitlines()[0].split(',')

def calculate_hash(step_key):
    step_result = 0
    for ascii in step_key:
        number = ord(ascii)
        step_result += number
        step_result *= 17
        step_result %= 256
    return step_result

def verify_result(box_lenses):
    result = 0
    for box_number, lenses in enumerate(box_lenses):
        for slot_in_box, (key, focal_length) in enumerate(lenses.items()):
            result += (box_number + 1) * (slot_in_box + 1) * focal_length
    return result

box_lenses = [{} for i in range(256)]

for step in line:

    if step[-1] == '-':
        step_key = step[:-1]
        index = calculate_hash(step_key)
        box_lenses[index].pop(step_key, None)

    else:
        step_key, value = step.split('=')
        index = calculate_hash(step_key)
        box_lenses[index][step_key] = int(value)

result = verify_result(box_lenses)
print(result)