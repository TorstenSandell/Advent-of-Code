from functools import reduce
from operator import mul
import pathlib
from typing import List

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

def convert_to_int_and_split_around_empty(numbers_list: List[str]):
    number_split_list = [[]]
    for number in numbers_list:
        n = number.strip()
        if n == "":
            number_split_list.append([])
            continue
        number_split_list[-1].append(int(number))
    return number_split_list

print(sum(sum(numbers) if method == "+" else reduce(mul, numbers) for numbers, method in zip(convert_to_int_and_split_around_empty(map("".join, map(list, zip(*raw_data[:-1])))), raw_data[-1].split())))