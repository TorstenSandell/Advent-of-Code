import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./9th/problem_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

histories = [[int(value) for value in line.split(" ")] for line in lines]
result = 0

for history in histories:
    found = False
    diffs = [history]
    i = 1
    while not found:
        diffs += [[diffs[i-1][position + 1] - diffs[i-1][position] for position in range(len(diffs[i-1]) - 1)]]
        found = True
        for diff in diffs[i]:
            if diff != 0:
                found = False
        i += 1

    for i in reversed(range(1, len(diffs))):
        this_diff = diffs[i]
        next_diff = diffs[i-1]

        new_history = next_diff[0] - this_diff[0]
        diffs[i-1] = [new_history] + next_diff

    result += diffs[0][0]

print(result)
    