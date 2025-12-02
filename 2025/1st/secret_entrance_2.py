from math import floor as fl

with open("./2025/1st/secret_entrance_input.txt", mode="r") as input:
    lines = input.read().splitlines()

operations = [-int(line[1:]) if line[0] == "L" else int(line[1:]) for line in lines]

val = 50
code = 0

def print_and_return(value):
    print(value)
    return value

for o in operations:
    val += o
    if val > 99:
        code += int(val / 100)
    if val <= 0:
        code += int(abs(val) / 100)
        if val - o != 0:
            code += 1

    val = val % 100


print(code)