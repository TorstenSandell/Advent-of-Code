import pathlib

########## Modifyables ##########

use_test_input = False
debug = False
splitchar = "\n"

#################################


def pr(value):
    if debug:
        print("  " + str(value))
    return value

path = pathlib.Path(__file__).parent.resolve()
input_file = "input.txt" if not use_test_input else "test.txt"
with open(f"{path}/{input_file}", mode="r") as input:
    raw_data = input.read().split(splitchar)

########## Write code below ##########

data = pr([d for d in raw_data])

def get_largest_digit(start_index, battery, end_index):
    largest_index = 0
    largest = 0

    battery_scope = battery[start_index:-end_index] if end_index > 0 else battery[start_index:]

    for i, value in enumerate(battery_scope):
        digit = int(value)
        if digit > largest:
            largest = digit
            largest_index = i
        if largest == 9:
            break
    return (largest_index+1+start_index, largest)

total_joltage = 0
for d in data:
    joltage_length = 12
    next_start_idx = 0
    joltage = 0
    for magnitude in range(joltage_length, 0, -1):
        next_start_idx, digit = get_largest_digit(next_start_idx, d, magnitude-1)
        joltage += digit * 10 ** (magnitude-1)
    total_joltage += pr(joltage)

print(total_joltage)