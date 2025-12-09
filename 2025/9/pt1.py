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
red_tiles = [tuple(map(int, d.split(","))) for d in raw_data]
print(max([(abs(first[0] - second[0]) + 1) * (abs(first[1] - second[1]) + 1) for first in red_tiles for second in red_tiles]))