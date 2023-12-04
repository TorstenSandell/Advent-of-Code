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

def find_gear_ratios(symbol_indices, number_indices):
    gear_ratios = []
    for i in range(len(symbol_indices)):
        for symbol in symbol_indices[i]:
            values_found = []
            for j in range(i-1, i+2):
                    if j < 0 or j >= len(number_indices):
                        continue
                    for number in number_indices[j]:
                        if number[1]-1 <= symbol and symbol <= number[2]:
                            values_found += [number[0]]
            if len(values_found) == 2:
                gear_ratios += [values_found[0] * values_found[1]]
                
    return gear_ratios

symbol_indices = []
number_indices = []

for line in lines:
    symbol_indices += [find_symbol(line)]
    number_indices += [find_numbers(line)]
    
gear_ratios = find_gear_ratios(symbol_indices, number_indices)
print(sum(gear_ratios))