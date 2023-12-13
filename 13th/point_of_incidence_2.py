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

def has_smudge(line1, line2):
    #print("checking for smudge")
    #print(line1, line2)
    not_found_diff = True
    for char1, char2 in zip(line1, line2):
        if char1 != char2 and not_found_diff:
            not_found_diff = False
        elif char1 != char2 and not not_found_diff:
            #print(f"found smudge: {False}")
            return False
    #print(f"found smudge: {not not_found_diff}")
    return not not_found_diff

def find_symmetry(problem):
    for i in range(len(problem) - 1):
        index_of_last_reflection = min(2 * i + 1, len(problem) - 1)
        index_of_first_reflection = max(0, i - (index_of_last_reflection - i) + 1)

        found_symmetry = True
        fixed_smudge = False

        for lower_index, upper_index in zip(range(index_of_first_reflection, i + 1), reversed(range(i + 1, index_of_last_reflection + 1))):
            #print(f"comparing {lower_index} with {upper_index}:")
            #print(problem[lower_index], problem[upper_index])
            line1 = problem[lower_index]
            line2 = problem[upper_index]
            if line1 != line2:
                if not fixed_smudge and has_smudge(line1, line2):
                    fixed_smudge = True
                else:        
                    found_symmetry = False
                    break

        if found_symmetry and fixed_smudge:
            return i + 1
    return 0

result = 0
found_symmetries = set({})

for nr, problem in enumerate(promblems_rows):
    #print("")
    #for row in problem:
        #print(row)
    r = find_symmetry(problem)
    if r > 0:
        found_symmetries.add(nr)
    #print(r)
    result += r * 100

#print("___________________________________-")
for nr, problem in enumerate(problem_cols):
    if nr not in found_symmetries:
        #print("")
        #for col in problem:
            #print(col)
        r = find_symmetry(problem)
        #print(r)
        result += r

print(result)
