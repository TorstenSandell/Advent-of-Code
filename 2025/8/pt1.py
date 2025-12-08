from functools import reduce
from math import sqrt
from operator import mul
import pathlib
from typing import List, Set

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

data = [tuple(map(int, d.split(","))) for d in raw_data]

def distance(vec1: tuple, vec2: tuple):
    return sqrt(sum([(v1 - v2) ** 2 for v1, v2 in zip(vec1, vec2)]))

class Connection:
    def __init__(self, box1, box2):
        self.boxes: set = set([box1, box2])
        self.distance = distance(box1, box2)

    def __str__(self):
        return str(self.distance)

def build_shortest_distances_list():
    l: List[Connection] = []
    for box1 in data:
        for box2 in data:
            if box1 == box2:
                continue
            l.append(Connection(box1, box2))
    return sorted(l, key=lambda c : c.distance)[::2]

n_connections = 10 if use_test_input else 1000
n_made_connections = 0

ordered_data = build_shortest_distances_list()
circuits: List[Set] = []

for connection in ordered_data:
    if n_made_connections >= n_connections:
        break

    found_circuit = -1
    for i in range(len(circuits)):
        circuit = circuits[i]
        if len(connection.boxes.intersection(circuit)) != 0:
            if found_circuit != -1:
                circuits[found_circuit] = circuit.union(circuits[found_circuit])
                circuits[i] = None
            else:
                found_circuit = i
                circuits[i] = circuit.union(connection.boxes)

    circuits = list(filter(lambda c : c is not None, circuits))

    if found_circuit == -1:
        circuits.append(connection.boxes)
    n_made_connections += 1

pr(circuits)

print(reduce(mul, [pr(len(circuit)) for circuit in sorted(circuits, key=len, reverse=True)[:3]]))