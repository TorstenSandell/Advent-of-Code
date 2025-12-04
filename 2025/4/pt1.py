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

grid = [d for d in raw_data]

size_x = len(grid[0])
size_y = len(grid)

empty = '.'
roll = '@'

movable_rolls = 0

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_adjacent_poss(self):
        poss = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if x != self.x or y != self.y:
                    poss.append(Pos(x, y))
        return poss

def get_grid_value(pos: Pos):
    return grid[pos.y][pos.x]

def is_roll(pos: Pos):
    return 0 <= pos.y < size_y and 0 <= pos.x < size_x and get_grid_value(pos) == roll

def sum_adjacent_roll_spaces(pos: Pos):
    return sum([1 if is_roll(p) else 0 for p in pos.get_adjacent_poss()])

for x in range(size_x):
    for y in range(size_y):
        p = Pos(x, y)
        if is_roll(p) and pr(sum_adjacent_roll_spaces(p)) < 4:
            movable_rolls += 1

print(movable_rolls)