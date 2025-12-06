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

line_length = len(raw_data[0])

class Problem:
    def __init__(self, values: List[str], method):
        self.values = [int(v) for v in values]
        self.method = method

def combine_cephalopod_number(data: List[str], index: int) -> int | None:
    number_str: str = pr("".join([d[index] for d in data]).strip())
    if number_str == "":
        return None
    return int(number_str)

def build_next_cephalopod_problem(data, start_index):
    problem_numbers = []
    method = data[-1][start_index]
    index = start_index
    while index < line_length:
        number = combine_cephalopod_number(data[:-1], index)
        index += 1
        if number is None:
            break
        problem_numbers.append(number)

    return index, Problem(pr(problem_numbers), method)

def build_cephalopod_problems(data: List) -> List[Problem]:
    problems = []
    all_built = False
    next_start_index = 0
    while not all_built:
        next_start_index, problem = build_next_cephalopod_problem(data, next_start_index)
        problems.append(problem)
        all_built = next_start_index >= line_length
    return problems

problems: List[Problem] = build_cephalopod_problems(raw_data)

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