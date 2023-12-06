import re
from math import sqrt, floor, ceil

with open("./6th/wait_for_it_input.txt", mode='r', encoding='utf-8') as input:
    lines = input.read().splitlines()

times = re.split(r"\s+", re.sub(r"Time:\s+", "", lines[0]))
distances = re.split(r"\s+", re.sub(r"Distance:\s+", "", lines[1]))

max_time = int("".join(times))
min_distance = int("".join(distances))

"""
speed = t
distance = speed*(t_max - t) = t*t_max - t^2

t_limit^2 - t_limit * t_max + min_distance = 0

t_limit = t_max/2 +- sqrt(t_max^2/4 - min_distance)

"""

t_upper_limit = max_time/2 + sqrt(max_time**2 / 4 - min_distance)
t_lower_limit = max_time/2 - sqrt(max_time**2 / 4 - min_distance)

# non-inclusive to limits
rounded_upper = ceil(t_upper_limit) - 1
rounded_lower = floor(t_lower_limit) + 1

# include all values
result = rounded_upper - rounded_lower + 1

print(result)