import pathlib

########## Modifyables ##########

use_test_input = True
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

data = [d for d in raw_data]