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

def print_grid(grid):
    if debug:
        print("\n".join(["".join(g) for g in grid]))

path = pathlib.Path(__file__).parent.resolve()
input_file = "input.txt" if not use_test_input else "test.txt"
with open(f"{path}/{input_file}", mode="r") as input:
    raw_data = input.read().split(splitchar)

########## Write code below ##########

diagram = [list(d) for d in raw_data]

start = "S"
beam = "|"
splitter = "^"

def _track_beam(row, col):
    if row >= len(diagram) or col >= len(diagram[0]) or col < 0:
        return 0
    value = pr(diagram[row][col])
    pr(f"({row} ,{col}): {value}")
    if value == beam:
        return 0
    elif value == splitter:
        return _track_beam(row, col-1) + _track_beam(row, col+1) + 1
    else:
        diagram[row][col] = beam
        return _track_beam(row+1, col)

def track_beam(start_col) -> int:
    return _track_beam(1, start_col)

print(track_beam(diagram[0].index(start)))
print_grid(diagram)