import pathlib
from typing import Iterator, List, Tuple
from itertools import groupby

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

def remove_duplicates(l: List):
    return [k for k, _ in groupby(sorted(l))]

class Present:

    def _rotate_shape(self, shape):
        new_shape = [False] * 9
        new_shape[0] = shape[6]
        new_shape[1] = shape[3]
        new_shape[2] = shape[0]
        new_shape[3] = shape[7]
        new_shape[4] = shape[4]
        new_shape[5] = shape[1]
        new_shape[6] = shape[8]
        new_shape[7] = shape[5]
        new_shape[8] = shape[2]
        return new_shape
        
    def _flip_shape(self, shape):
        new_shape = [False] * 9
        new_shape[0] = shape[2]
        new_shape[1] = shape[1]
        new_shape[2] = shape[0]
        new_shape[3] = shape[5]
        new_shape[4] = shape[4]
        new_shape[5] = shape[3]
        new_shape[6] = shape[8]
        new_shape[7] = shape[7]
        new_shape[8] = shape[6]
        return new_shape


    def __init__(self, data: List[str]):
        shape = [value == "#" for line in data for value in line]
        all_shapes = []
        for _ in range(2):
            for _ in range(4):
                all_shapes.append(shape)
                shape = self._rotate_shape(shape)
            shape = self._flip_shape(shape)
        self.shapes = remove_duplicates(all_shapes)
    
    def size(self):
        return sum([1 if filled else 0 for filled in self.shapes[0]])

n_presents = 6
present_data_length = 5
presents: List[Present] = []
for i in range(n_presents):
    start_line = i * present_data_length + 1
    end_line = start_line + present_data_length - 2
    presents.append(Present(raw_data[start_line:end_line]))

class Grid:

    def __init__(self, data_line: str):
        split_line = data_line.split(" ")
        dimensions = split_line[0][:-1].split("x")
        self.width = int(dimensions[0])
        self.height = int(dimensions[1])
        self.present_amounts = list(map(int, split_line[1:]))
        self.grid_layout = [False] * (self.height * self.width)

    def index_shape_iterator(self, index) -> Iterator[Tuple[int, int]]:
        for shape_index in range(9):
            grid_index = shape_index if shape_index < 3 else (shape_index % 3 + self.width if shape_index < 6 else shape_index % 3+ 2 * self.width)
            yield shape_index, grid_index + index

    def fit_shape(self, shape, index):
        if index % self.width > self.width - 3 or int(index / self.width) > self.height - 3:
            return False
        for shape_index, grid_index in self.index_shape_iterator(index):
            if shape[shape_index] and self.grid_layout[grid_index]:
                return False
        return True

    def place_shape(self, shape, index):
        if not self.fit_shape(shape, index):
            return False
        for shape_index, grid_index in self.index_shape_iterator(index):
            self.grid_layout[grid_index] = shape[shape_index]
        return True
    
    def remove_shape(self, shape, index):
        for shape_index, grid_index in self.index_shape_iterator(index):
            if shape[shape_index]:
                self.grid_layout[grid_index] = False

    def _get_wanted_shapes(self):
        shapes = []
        for present_index in range(n_presents):
            if self.present_amounts[present_index] > 0:
                shapes += presents[present_index].shapes
        return shapes

    def sanity_check_impossible_grid(self):
        return sum([amount * present.size() for amount, present in zip(self.present_amounts, presents)]) > self.width * self.height

    def _resolve(self, index):
        shapes = self._get_wanted_shapes()
        if not shapes:
            return True

        while index < self.width * self.height:
            for shape in shapes:
                if self.place_shape(shape, index):
                    if self._resolve(index+1):
                        return True
                    self.remove_shape(shape, index)
            index += 1
        return False

    def resolve(self):
        if self.sanity_check_impossible_grid():
            return 0
        self._resolve(0)


data_split_line_index = n_presents * present_data_length
grids: List[Grid] = [Grid(d) for d in raw_data[data_split_line_index:]]
print(sum([g.resolve() for g in grids]))
for g in grids:
    print(g.grid_layout)