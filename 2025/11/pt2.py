import pathlib
from typing import Dict, List, Set

########## Modifyables ##########

use_test_input = True
debug = True
splitchar = "\n"

#################################


def pr(value):
    if debug:
        print("  " + str(value))
    return value

path = pathlib.Path(__file__).parent.resolve()
input_file = "input.txt" if not use_test_input else "test2.txt"
with open(f"{path}/{input_file}", mode="r") as input:
    raw_data = input.read().split(splitchar)

########## Write code below ##########

start_value = "svr"
end_value = "out"
need_passed = {"dac", "fft"}
data: Dict[str, List[str]] = {line[0][:-1]: line[1:] for line in [d.split(" ") for d in raw_data]}

class PathValues:
    def __init__(self):
        self.prerequisite_dict = [None, None, None, None]
    def _get_index(self, visited: Set):
        overlap_set = visited.intersection(need_passed)
        if len(overlap_set) == 2:
            return 0
        if len(overlap_set) == 0:
            return 1
        if list(overlap_set)[0] == "dac":
            return 2
        if list(overlap_set)[0] == "fft":
            return 3
        return 4  # error


    def update(self, visited: Set, subsequent_valid_paths):
        self.prerequisite_dict[self._get_index(visited)] = subsequent_valid_paths

    def get(self, visited: Set):
        return self.prerequisite_dict[self._get_index(visited)]

calculated_paths: Dict[str, PathValues] = dict({})

def _find_paths_to_end(current, visited: Set[str]):
    if current in visited:
        return 0
    elif current == end_value:
        return 1 if visited.intersection(need_passed) == need_passed else 0
    elif current in calculated_paths:
        already_calculated_value = calculated_paths[current].get(visited)
        if already_calculated_value is not None:
            return already_calculated_value  # Already calculated
    else:
        calculated_paths[current] = PathValues()

    visited.add(current)
    subsequent_paths = sum([_find_paths_to_end(next_connected, visited) for next_connected in data[current]])
    calculated_paths[current].update(visited, subsequent_paths)
    visited.remove(current)

    return subsequent_paths

def find_paths_to_end():
    visited = set([])
    visited.add(start_value)
    return sum([_find_paths_to_end(next_connected, visited) for next_connected in data[start_value]])

print(find_paths_to_end())