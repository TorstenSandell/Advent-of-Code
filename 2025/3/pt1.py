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

total_joltage = 0
for d in data:
    largest_first_index = 0
    largest_first = 0
    largest_second = 0

    for i, value in enumerate(d[:-1]):
        first_digit = int(value)
        if first_digit > largest_first:
            largest_first = first_digit
            largest_first_index = i
        if largest_first == 9:
            break

    for value in d[largest_first_index+1:]:
        second_digit = int(value)
        if second_digit > largest_second:
            largest_second = second_digit
        if largest_second == 9:
            break

    total_joltage += pr(10 * largest_first + largest_second)

print(total_joltage)