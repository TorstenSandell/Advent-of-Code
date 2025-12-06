from dataclasses import dataclass
import pathlib
from typing import List

@dataclass
class Global:
    debug = False
    use_test_input = True

def pr(value):
    if Global.debug:
        print("  " + str(value))
    return value

def get_raw_data_file_contents(file):
    path = pathlib.Path(file).parent.resolve()
    input_file = "input.txt" if not Global.use_test_input else "test.txt"
    with open(f"{path}/{input_file}", mode="r") as input:
        return input.read()

def transpose(matrix: List[List]):
    return map(list, zip(*matrix))