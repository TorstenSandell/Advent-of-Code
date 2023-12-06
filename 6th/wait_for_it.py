import re

with open("./6th/wait_for_it_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

times = re.split(r"\s+", re.sub(r"Time:\s+", "", lines[0]))
distances = re.split(r"\s+", re.sub(r"Distance:\s+", "", lines[1]))

result = 1

for i in range(len(times)):
    time = int(times[i])
    distance = int(distances[i])

    ways_to_win = 0
    for speed in range(time + 1):
        t = time - speed
        d = t * speed
        if d > distance:
            ways_to_win += 1
    result *= ways_to_win

print(result)