

debug = False

with open("./2025/2nd/input.txt", mode="r") as input:
    lines = input.read().split(',')

ranges = [tuple(line.split('-')) for line in lines]

def pr(value):
    if debug:
        print("  " + str(value))
    return value

sum_invalid = 0
for start, stop in ranges:
    for value in range(int(start), int(stop)+1):
        n_digits = len(str(value))
        if n_digits % 2 == 1:
            continue
        breakv = 10 ** (n_digits / 2)
        if pr(int(value / breakv)) == pr(value % breakv):
            sum_invalid += value

print(sum_invalid)