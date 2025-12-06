import pathlib
from typing import List

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

data = [d.split() for d in raw_data]

class Problem:
    def __init__(self, values: List[str], method):
        self.values = [int(v) for v in values]
        self.method = method

problems: List[Problem] = [Problem(d[:-1], d[-1]) for d in map(list, zip(*data))]

class Operators:
    multiplication = "*"
    addition = "+"

def prod(numbers: List[int]):
    result = 1
    for value in numbers:
        result *= value
    return result

def calculate(problem: Problem):
    match problem.method:
        case Operators.multiplication:
            return prod(problem.values)
        case Operators.addition:
            return sum(problem.values)

print(sum(pr(calculate(problem)) for problem in problems))