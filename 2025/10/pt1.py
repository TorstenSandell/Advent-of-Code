from itertools import chain, combinations
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

def iter_powerset(s: Set[T]) -> Iterable[Set[T]]:
    return chain.from_iterable(combinations(s, length) for length in range(1, len(s)))


class LightDiagram:
    def __init__(self, raw_data_line: str):
        data_line = raw_data_line.split(" ")
        self.light_config = [conf == "#" for conf in data_line[0][1:-1]]
        self.buttons = set([tuple(map(int, button_spec[1:-1].split(","))) for button_spec in data_line[1:-1]])

    def _combine_buttons(self, button_set: Set[Tuple[int]]) -> List[bool]:
        resulting_lighting = [False] * len(self.light_config)
        for button in button_set:
            for button_toggle in button:
                resulting_lighting[button_toggle] = not resulting_lighting[button_toggle]
        return resulting_lighting

    def find_lowest_button_combination_count(self) -> int:
        for button_set in iter_powerset(self.buttons):
            if self._combine_buttons(button_set) == self.light_config:
                return len(button_set)

print(sum([pr(d.find_lowest_button_combination_count()) for d in [LightDiagram(raw_data_line) for raw_data_line in raw_data]]))