import pathlib
from typing import List, Self

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

class IngredientRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def overlaps(self, other: Self):
        return self.start <= other.stop and self.stop >= other.start or \
               self.stop >= other.start and self.start <= other.stop

    def union(self, range_union: List[Self]):
        inserted = False
        for i in range(len(range_union)):
            other = range_union[i]
            if self.overlaps(other):
                self.start = min(self.start, other.start)
                self.stop = max(self.stop, other.stop)
                range_union[i] = self  # Override
                inserted = True

        if inserted:
            indices_to_be_deleted = []
            found_first = False
            for i in range(len(range_union)):
                if range_union[i] == self:
                    if found_first:
                        indices_to_be_deleted.append(i)
                    found_first = True

            for i in indices_to_be_deleted:
                range_union.pop(i)

        else:
            range_union.append(self)


range_union_list: List[IngredientRange] = []

for data in raw_data:
    if data == "":
        break

    start, stop = data.split('-')
    IngredientRange(int(start), int(stop)).union(range_union_list)

total_fresh = 0
for r in range_union_list:
    total_fresh += r.stop - r.start + 1

print(total_fresh)
