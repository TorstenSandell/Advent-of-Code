from typing import List

def transpose(matrix: List[List]):
    return map(list, zip(*matrix))