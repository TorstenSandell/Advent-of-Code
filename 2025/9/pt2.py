from enum import Enum
import pathlib
from typing import Dict, Iterable, List, Tuple, TypeVar

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



corner_tile = "#"
edge_tile = "X"
surface_tile = "W"
uncolored_tile = "."
colored_tiles = set([corner_tile, edge_tile, surface_tile])

T = TypeVar('T')

class PosState(Enum):
    OUTSIDE = 0
    INSIDE = 1
    EDGE_FROM_INSIDE = 2
    EDGE_FROM_OUTSIDE = 3

class DrawingStateMachine:

    def __init__(self):
        self.state = PosState.OUTSIDE
        self.last_corner_was_positive = False

    
    def corner_is_positive(self, x: int, y: int, reduced_red_tiles: List[Tuple[int]]):
        index = reduced_red_tiles.index((x, y))
        if reduced_red_tiles[(index - 1) % len(reduced_red_tiles)][1] == y:
            return x - reduced_red_tiles[index - 1][0] > 0
        return x - reduced_red_tiles[(index + 1) % len(reduced_red_tiles)][0] > 0


    def update_state(self, x: int, y: int, grid: List[List[str]], reduced_red_tiles: List[Tuple[int]]):
        curr_tile = grid[x][y]
        if curr_tile == edge_tile:
            if self.state == PosState.OUTSIDE:
                self.state = PosState.INSIDE
            elif self.state == PosState.INSIDE:
                self.state = PosState.OUTSIDE
        elif curr_tile == corner_tile:
            if self.state == PosState.OUTSIDE:
                self.state = PosState.EDGE_FROM_OUTSIDE
                self.last_corner_was_positive = self.corner_is_positive(x, y, reduced_red_tiles)
            elif self.state == PosState.INSIDE:
                self.state = PosState.EDGE_FROM_INSIDE
                self.last_corner_was_positive = self.corner_is_positive(x, y, reduced_red_tiles)
            elif self.state == PosState.EDGE_FROM_OUTSIDE:
                if self.last_corner_was_positive != self.corner_is_positive(x, y, reduced_red_tiles):
                    self.state = PosState.INSIDE
                else:
                    self.state = PosState.OUTSIDE
            elif self.state == PosState.EDGE_FROM_INSIDE:
                if self.last_corner_was_positive != self.corner_is_positive(x, y, reduced_red_tiles):
                    self.state = PosState.OUTSIDE
                else:
                    self.state = PosState.INSIDE


def wrapping_pair_iterator(iterable: Iterable[T]) -> Iterable[T]:
    for i in range(len(iterable)):
        yield (iterable[i - 1], iterable[i])

def range_from_to_exclusive(f: int, t: int) -> range:
    return range(f+1, t) if f < t else range(t+1, f)

def range_from_to_inclusive(f: int, t: int) -> range:
    return range(f, t+1) if f < t else range(t, f+1)

def create_reduced_grid_size_conversion_dict(red_tiles):
    reduced_red_tiles_dict = {tile: [-1, -1] for tile in red_tiles}

    for i in range(2):
        last_tile = None
        value_to_insert = 0

        for current_tile in sorted(red_tiles, key=lambda t : t[i]):

            if last_tile is not None:
                diff_last = current_tile[i] - last_tile[i]
                value_to_insert += diff_last if diff_last < 2 else 2

            reduced_red_tiles_dict[current_tile][i] = value_to_insert
            last_tile = current_tile

    return {key: tuple(reduced_red_tiles_dict[key]) for key in reduced_red_tiles_dict.keys()}

def create_grid(red_tiles: List[Tuple[int]], reduced_red_tiles_conversion: Dict[Tuple[int], Tuple[int]]):
    len_x = max(reduced_red_tiles_conversion.values(), key=lambda t : t[0])[0] + 1
    len_y = max(reduced_red_tiles_conversion.values(), key=lambda t : t[1])[1] + 1

    grid = [[uncolored_tile for _ in range(len_y)] for _ in range(len_x)]

    
    for last_tile, tile in wrapping_pair_iterator(red_tiles):
        x, y = reduced_red_tiles_conversion[tile]
        last_x, last_y = reduced_red_tiles_conversion[last_tile]
        grid[x][y] = corner_tile

        for xi in range_from_to_exclusive(last_x, x):
            grid[xi][y] = edge_tile
        for yi in range_from_to_exclusive(last_y, y):
            grid[x][yi] = edge_tile
    
    reduced_red_tiles = [reduced_red_tiles_conversion[key] for key in red_tiles]

    for x in range(len_x):
        sm = DrawingStateMachine()
        for y in range(len_y):
            sm.update_state(x, y, grid, reduced_red_tiles)
            if sm.state == PosState.INSIDE and grid[x][y] == uncolored_tile:
                grid[x][y] = surface_tile
    return grid

def validate_rectangle(tile_1: Tuple[int], tile_2: Tuple[int], reduced_red_tiles_conversion: Dict[Tuple[int], Tuple[int]], grid: List[List[str]]) -> bool:
    t1 = reduced_red_tiles_conversion[tile_1]
    t2 = reduced_red_tiles_conversion[tile_2]
    for x in range_from_to_inclusive(t1[0], t2[0]):
        for y in range_from_to_inclusive(t1[1], t2[1]):
            if grid[x][y] == uncolored_tile:
                return False
    return True

def calculate_rectangle(tile_1: Tuple[int], tile_2: Tuple[int]):
    return (abs(tile_1[0] - tile_2[0]) + 1) * (abs(tile_1[1] - tile_2[1]) + 1)

red_tiles = [tuple(map(int, d.split(","))) for d in raw_data]
reduced_red_tiles_conversion = create_reduced_grid_size_conversion_dict(red_tiles)
grid = create_grid(red_tiles, reduced_red_tiles_conversion)
for line in grid:
    pr("".join(line))

print(max([calculate_rectangle(t1, t2) if validate_rectangle(t1, t2, reduced_red_tiles_conversion, grid) else 0 for t2 in red_tiles for t1 in red_tiles]))
