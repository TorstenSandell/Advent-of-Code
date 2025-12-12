import pathlib
from typing import Dict, List, Set

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

start_value = "you"
end_value = "out"
data: Dict[str, List[str]] = {line[0][:-1]: line[1:] for line in [d.split(" ") for d in raw_data]}
calculated: Dict[str, int] = dict({})

def _find_paths_to_end(current, end, visited: Set[str]):
    if current in visited:
        return 0
    elif current == end:
        return 1
    elif current in calculated:
        return calculated[current]
    visited.add(current)
    subsequent_paths = sum([_find_paths_to_end(next_connected, end, visited) for next_connected in data[current]])
    calculated[current] = subsequent_paths
    visited.remove(current)
    return subsequent_paths

def find_paths_to_end(start, end):
    visited = set([])
    visited.add(start)
    return sum([_find_paths_to_end(next_connected, end, visited) for next_connected in data[start]])

print(find_paths_to_end(start_value, end_value))