with open("./2025/1st/secret_entrance_input.txt", mode="r") as input:
    lines = input.read().splitlines()

operations = [-int(line[1:]) if line[0] == "L" else int(line[1:]) for line in lines]
val = 50
code = 0
for o in operations:
    val = (val + o) % 100
    if val == 0:
        code += 1

print(code)