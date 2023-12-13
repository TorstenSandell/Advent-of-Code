import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./13th/point_of_incidence_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()


promblems_rows = [[]]
i = 0
for line in lines:
    if line == '':
        i += 1
        promblems_rows += [[]]
    else:
        promblems_rows[i] += [line]

problem_cols = []
for problem in promblems_rows:
    cols = []
    has_added_base = False
    for row in problem:
        for col, value in enumerate(row):
            if has_added_base:
                cols[col] += value
            else:
                cols += [value]
        has_added_base = True
    problem_cols += [cols]


def find_symmetry(problem):
    for i in range(len(problem) - 1):
        index_of_last_reflection = min(2 * i + 1, len(problem) - 1)
        index_of_first_reflection = max(0, i - (index_of_last_reflection - i) + 1)

        found_symmetry = True

        for lower_index, upper_index in zip(range(index_of_first_reflection, i + 1), reversed(range(i + 1, index_of_last_reflection + 1))):
            #print(f"comparing {lower_index} with {upper_index}:")
            #print(problem[lower_index], problem[upper_index])
            if problem[lower_index] != problem[upper_index]:
                found_symmetry = False
                break

        if found_symmetry:
            return i + 1
    return 0

result = 0
for problem in promblems_rows:
    #print("")
    #for row in problem:
        #print(row)
    r = find_symmetry(problem)
    #print(r)
    result += r * 100

#print("___________________________________-")
for problem in problem_cols:
    #print("")
    #for col in problem:
        #print(col)
    r = find_symmetry(problem)
    #print(r)
    result += r

print(result)
