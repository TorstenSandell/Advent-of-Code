import pathlib
from typing import Generic, Iterable, List, Self, Set, Tuple, TypeVar

########## Modifyables ##########

use_test_input = False
debug = True
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

T = TypeVar('T')
MAY_HAVE_CANCELLING_EDGES = False

def pair_iterator(iterable: Iterable[T]) -> Iterable[T]:
    for i in range(len(iterable)):
        yield (iterable[i - 1], iterable[i])

def iterate_all_from_index(l: List[T], index: int) -> Iterable[T]:
    length = len(l)
    for i in range(length):
        yield l[(i + index + 1) % length]

def rotate_positive(t: Tuple[int]) -> Tuple[int]:
    return (t[1], -t[0])

def rotate_negative(t: Tuple[int]) -> Tuple[int]:
    return (-t[1], t[0])

def shrink_to_unit(n: int) -> int:
    return n / abs(n) if n != 0 else 0

def normalize(t: Tuple[int]) -> Tuple[int]:
    return (shrink_to_unit(t[0]), shrink_to_unit(t[1]))

class Edge:
    def __init__(self, tile1: Tuple[int], tile2: Tuple[int]):
        self.tiles = set([tile1, tile2])
        self.outside_direction = (0, 0)  # To be set to (1, 0), (0, 1), (-1, 0) or (-1, 0) later

    def get_endpoints(self) -> Tuple[Tuple[int]]:
        return tuple(self.tiles)
    
    def is_within(self, t1: Tuple[int], t2: Tuple[int]):
        e1, e2 = self.get_endpoints()
        has_x_endpoint_within = t1[0] < e1[0] < t2[0] or t1[0] > e1[0] > t2[0] or t1[0] < e2[0] < t2[0] or t1[0] > e2[0] > t2[0]
        has_y_endpoint_within = t1[1] < e1[1] < t2[1] or t1[1] > e1[1] > t2[1] or t1[1] < e2[1] < t2[1] or t1[1] > e2[1] > t2[1]
        has_endpoint_within = has_x_endpoint_within and has_y_endpoint_within
        slices_through_x = has_y_endpoint_within and (e1[0] <= t1[0] <= t2[0] <= e2[0] or
                                                      e1[0] >= t1[0] >= t2[0] >= e2[0] or
                                                      e1[0] <= t2[0] <= t1[0] <= e2[0] or
                                                      e1[0] >= t2[0] >= t1[0] >= e2[0])
        slices_through_y = has_x_endpoint_within and (e1[1] <= t1[1] <= t2[1] <= e2[1] or
                                                      e1[1] >= t1[1] >= t2[1] >= e2[1] or
                                                      e1[1] <= t2[1] <= t1[1] <= e2[1] or
                                                      e1[1] >= t2[1] >= t1[1] >= e2[1]) 
        slices_through = slices_through_x or slices_through_y
        return has_endpoint_within or slices_through

class Vector:
    def __init__(self, point: Tuple[int], direction: Tuple[int]):
        self.point: Tuple[int] = point
        self.direction: Tuple[int] = direction

    def intersects_with(self, edge: Edge):
        """Checks for intersection with edge. If start point is on the edge but the direction is not parallel, it does not count as an intersection."""
        e1, e2 = edge.get_endpoints()
        within_dim = self.direction.index(0)
        intersects_dimensionally = e1[within_dim] <= self.point[within_dim] <= e2[within_dim] or e1[within_dim] >= self.point[within_dim] >= e2[within_dim]
        within_dir = 0 if within_dim == 1 else 1
        intersects_directionally = e1[within_dir] > self.point[within_dir] < e2[within_dir] if self.direction[within_dir] == 1 else e1[within_dir] < self.point[within_dir] > e2[within_dir]
        return intersects_dimensionally and intersects_directionally


class Corner:
    def __init__(self, edge1: Edge, edge2: Edge):
        assert len(edge1.tiles.intersection(edge2.tiles)) == 1
        assert not any([t1p == t2p == t3p for t1p, t2p, t3p in zip(*(edge1.tiles.union(edge2.tiles)))])  # No corner in straight lines
        self.edges: Set[Edge] = set([edge1, edge2])
        self.corner_tile: Tuple[int] = edge1.tiles.intersection(edge2.tiles).pop()
        self.outside_direction = (0, 0)

    def _get_edge_direction_given_that_this_points_outside(self, edge: Edge) -> Tuple[int]:
        assert edge in self.edges
        other_edge_tile = edge.tiles.symmetric_difference(set([self.corner_tile])).pop()
        return normalize((self.corner_tile[0] - other_edge_tile[0], self.corner_tile[1] - other_edge_tile[1]))

    def _unpack_edges(self) -> Tuple[Edge]:
        return tuple(self.edges)

    def points_outside_guaranteed(self, all_edges: List[Edge]):
        for edge in self.edges:
            direction = self._get_edge_direction_given_that_this_points_outside(edge)
            v: Vector = Vector(self.corner_tile, direction)
            if any([v.intersects_with(e) for e in all_edges]):
                return False
        return True
    
    def define_as_outside(self):
        for edge in self.edges:
            edge.outside_direction = self._get_edge_direction_given_that_this_points_outside(edge)
            self.outside_direction = (self.outside_direction[0] + edge.outside_direction[0], self.outside_direction[1] + edge.outside_direction[1])

    def propagate_outside(self):
        e1, e2 = self._unpack_edges()
        edge_from: Edge = e1 if e1.outside_direction != (0, 0) else e2
        edge_to: Edge = e2 if edge_from == e1 else e1
        corner_outside_vector: Vector = Vector(self.corner_tile, edge_from.outside_direction)
        edge_to.outside_direction = rotate_negative(edge_from.outside_direction) if corner_outside_vector.intersects_with(edge_to) else rotate_positive(edge_from.outside_direction)
        self.outside_direction = (edge_from.outside_direction[0] + edge_to.outside_direction[0], edge_from.outside_direction[1] + edge_to.outside_direction[1])

    def outside_direction_is_set(self) -> bool:
        return self.outside_direction[0] != 0 and self.outside_direction[1] != 0

    def compatible_rectangle_corner(self, other: Self) -> bool:
        assert self.outside_direction_is_set() and other.outside_direction_is_set()
        return (self.corner_tile == other.corner_tile or
                self.corner_tile[0] == other.corner_tile[0] and self.outside_direction[0] != other.outside_direction[0] or
                self.corner_tile[1] == other.corner_tile[1] and self.outside_direction[1] != other.outside_direction[1] or
                self.outside_direction[1] != other.outside_direction[1] and self.outside_direction[0] != other.outside_direction[0])

    def rectangle_is_blocked(self, other: Self, all_edges: List[Edge]) -> bool:
        for edge in all_edges:
            if edge.is_within(self.corner_tile, other.corner_tile):
                return True
        return False

    def rectangle_size(self, other: Self, all_edges: List[Edge]) -> int:
        if not self.compatible_rectangle_corner(other) or self.rectangle_is_blocked(other, all_edges):
            return 0
        return (abs(self.corner_tile[0] - other.corner_tile[0]) + 1) * (abs(self.corner_tile[1] - other.corner_tile[1]) + 1)


class Grid:
    def __init__(self, raw_data):
        self.red_tiles: List[Tuple[int]] = [tuple(map(int, d.split(","))) for d in raw_data]
        self.edges: List[Edge] = [Edge(tile_pair[0], tile_pair[1]) for tile_pair in pair_iterator(self.red_tiles)]
        self.corners: List[Corner] = [Corner(edge_pair[0], edge_pair[1]) for edge_pair in pair_iterator(self.edges)]

    def setup_outside_directions(self):
        for corner in self.corners:
            if corner.points_outside_guaranteed(self.edges):
                break
        corner.define_as_outside()
        for c in iterate_all_from_index(self.corners, self.corners.index(corner)):
            c.propagate_outside()

g: Grid = Grid(raw_data)
pr("Grid created!")
g.setup_outside_directions()
pr("Outside set up!")
print(sum([1 if t1 != t2 and (t1[0] - t2[0] == 1 or t1[1] - t2[1] == 1) else 0 for t1 in g.red_tiles for t2 in g.red_tiles]))
print(max([corner1.rectangle_size(corner2, g.edges) for corner1 in g.corners for corner2 in g.corners]))