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

diagram = [list(d) for d in raw_data]

start = "S"
splitter = "^"

def reverse_range(start):
    return range(start-1, -1, -1)

reverse_timeline_diagram = ([[0] * len(diagram[0]) for _ in range(len(diagram) - 1) ])
reverse_timeline_diagram.append([1] * len(diagram[0]))

start_col = diagram[0].index(start)

def calculate_timeline(row, col):
    diagram_value = diagram[row][col]
    if diagram_value == splitter:
        reverse_timeline_diagram[row][col] = reverse_timeline_diagram[row+1][col-1] + reverse_timeline_diagram[row+1][col+1]
    else:
        reverse_timeline_diagram[row][col] = reverse_timeline_diagram[row+1][col]

for row in reverse_range(len(diagram)-1):
    for col in range(len(diagram[0])):
        calculate_timeline(row, col)

if debug: print("\n".join([str(r) for r in reverse_timeline_diagram]))
print(reverse_timeline_diagram[0][start_col])