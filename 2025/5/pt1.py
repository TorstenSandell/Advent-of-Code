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

ranges = []
ingredients = []
ranges_done = False

for data in raw_data:
    if data == "":
        ranges_done = True
        continue

    if not ranges_done:
        start, stop = data.split('-')
        ranges.append(range(int(start), int(stop)+1))
    else:
        ingredients.append(int(data))

total_fresh = 0

for ingredient in ingredients:
    for r in ranges:
        if ingredient in r:
            total_fresh += 1
            break

print(total_fresh)
