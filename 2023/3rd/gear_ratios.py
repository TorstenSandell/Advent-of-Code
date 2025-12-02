import re

with open("./3rd/gear_ratios_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

def find_symbol(line):
    resulting_indices = []
    for i in range(len(line)):
        if re.match(r'[^0-9.]', line[i]) is not None:
            resulting_indices += [i]
    return resulting_indices

def find_numbers(line):
    resulting_indices = []
    numbers = re.findall('\d+', line)
    start_index = 0
    for number in numbers:
        index = line.find(number, start_index)
        start_index = index + len(number)
        resulting_indices += [(int(number), index, start_index)]
    return resulting_indices

def find_matching_numbers(symbol_indices, number_indices):
    matching_numbers = []
    for i in range(len(number_indices)):
        for number in number_indices[i]:
            found = False
            for index in range(number[1] - 1, number[2] + 1):
                if found:
                    break
                for j in range(i-1, i+2):
                    if j < 0 or j >= len(symbol_indices):
                        continue
                    if index in symbol_indices[j]:
                        matching_numbers += [number[0]]
                        found = True
                        break
    return matching_numbers

symbol_indices = []
number_indices = []

for line in lines:
    symbol_indices += [find_symbol(line)]
    number_indices += [find_numbers(line)]
    
matches = find_matching_numbers(symbol_indices, number_indices)
print(sum(matches))