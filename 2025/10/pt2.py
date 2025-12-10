from itertools import chain, combinations_with_replacement
import pathlib
from typing import Iterable, List, Set, Tuple, TypeVar

########## Modifyables ##########

use_test_input = False
debug = True
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
T = TypeVar('T')

def iterate_to_infinity_and_beyond(start_value):
    value = start_value
    while True:
        yield value
        value += 1

def iter_combinations_with_replacement(s: Set[T]) -> Iterable[Set[T]]:
    return chain.from_iterable(combinations_with_replacement(s, length) for length in iterate_to_infinity_and_beyond(1))

class LightDiagram:
    def __init__(self, raw_data_line: str):
        data_line = raw_data_line.split(" ")
        self.power_config = tuple(map(int, data_line[-1][1:-1].split(",")))
        self.buttons = set([tuple(map(int, button_spec[1:-1].split(","))) for button_spec in data_line[1:-1]])

    def _combine_buttons(self, button_set: Set[Tuple[int]]) -> Tuple[int]:
        resulting_power = [0] * len(self.power_config)
        for button in button_set:
            for button_toggle in button:
                resulting_power[button_toggle] += 1
        return tuple(resulting_power)

    def find_lowest_button_combination_count(self) -> int:
        for button_set in iter_combinations_with_replacement(self.buttons):
            if self._combine_buttons(button_set) == self.power_config:
                return len(button_set)

diagrams: List[LightDiagram] = [LightDiagram(raw_data_line) for raw_data_line in raw_data]
print(sum([pr(d.find_lowest_button_combination_count()) for d in diagrams]))