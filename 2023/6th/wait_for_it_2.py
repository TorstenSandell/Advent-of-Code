import re

with open("./6th/wait_for_it_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

times = re.split(r"\s+", re.sub(r"Time:\s+", "", lines[0]))
distances = re.split(r"\s+", re.sub(r"Distance:\s+", "", lines[1]))

time = int("".join(times))
distance = int("".join(distances))

result = 0

# suboptimal solution, but is fast enough
for speed in range(time + 1):
    t = time - speed
    d = t * speed
    if d > distance:
        result += 1

print(result)