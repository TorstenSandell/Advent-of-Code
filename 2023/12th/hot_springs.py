import re
from math import sqrt, floor, ceil, gcd, inf
from collections import Counter

with open("./12th/hot_springs_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

condition_records = []
for line in lines:
    records, groupings = line.split(' ')
    condition_records += [(records, [int(group) for group in groupings.split(',')])]

def find_next_free_space(index, record):
    for i, char in enumerate(record[index:]):
        if char == '#' or char == '?':
            return i + index
        
def can_insert(index, record, grouping):
    if index + grouping > len(record):
        return False
    for r in record[index:index + grouping]:
        if r == '.':
            return False
    if '#' in record[:index]:
        return False
    if index + grouping < len(record) and record[index + grouping] == '#':
        return False
    return True 

def find_amount_of_valid_insertions_for(record, groupings, index, grouping_number, positions_to_combinations):
    if grouping_number >= len(groupings):
        if  not '#' in record:
            return 1
        else:
            return 0

    if (index, grouping_number) not in positions_to_combinations:

        positions_to_combinations[(index, grouping_number)] = 0
        free_spaces = set({})

        for i in range(index, len(record)):
            free_spaces.add(find_next_free_space(i, record))
        free_spaces.discard(None)

        for free_space in free_spaces:
            grouping = groupings[grouping_number]
            if can_insert(free_space, record, grouping):
                next_index = free_space + grouping + 1

                if next_index < len(record):
                    next_record = '!' * (free_space + grouping + 1) + record[next_index:]
                    positions_to_combinations[(index, grouping_number)] += find_amount_of_valid_insertions_for(next_record, groupings, next_index, grouping_number + 1, positions_to_combinations)
                elif grouping_number + 1 == len(groupings):  # the whole record should be covered if next_index >= len(record)
                    positions_to_combinations[(index, grouping_number)] += 1

    return positions_to_combinations[(index, grouping_number)]

def solve_for(record, groupings):
    positions_to_combinations = {}
    find_amount_of_valid_insertions_for(record, groupings, 0, 0, positions_to_combinations)
    result = 0
    for position, combination in positions_to_combinations.items():
        if position[1] == 0:
            result += combination
    return result

result = 0
for (record, groupings) in condition_records:
    result += solve_for(record, groupings)

print(result)