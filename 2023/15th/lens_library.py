import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./15th/lens_library_input.txt", mode='r', encoding='utf-8') as input:
    line = input.read().splitlines()[0].split(',')

result = 0
for step in line:
    step_result = 0
    for ascii in step:
        number = ord(ascii)
        step_result += number
        step_result *= 17
        step_result %= 256
    result += step_result
print(result)