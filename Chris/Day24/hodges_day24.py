import re
from enum import Enum
from typing import List
from operator import add

class Direction(Enum):
    e=(1, -1, 0)
    se=(0, -1, 1)
    sw=(-1, 0, 1)
    w=(-1, 1, 0)
    nw=(0, 1, -1)
    ne=(1, 0, -1)

class Coord(object):
    def __init__(self, x, y, z):
        self.coords = (x, y, z)

    def neighbor(self, direction: Direction) -> 'Coord':
        return Coord(*tuple(map(add, self.coords, direction.value)))

    def __repr__(self):
        return f"{self.coords[0]},{self.coords[1]},{self.coords[2]}"

    def __eq__(self, other):
        return self.coords == other.coords

    def __hash__(self):
        return hash(self.coords)


class Board(object):
    def __init__(self):
        self.grid = {}
    
    def ref_count_space(self, coord: Coord):
        if coord in self.grid:
            self.grid[coord] += 1
        else:
            self.grid[coord] = 1

    def traverse_path_from_origin(self, directions: List[Direction]) -> Coord:
        coord = Coord(0, 0, 0)
        for direction in directions:
            coord = coord.neighbor(direction)
        return coord

    def count_tiles_by_filter_function(self, fn) -> int:
        return len(list(filter(fn, self.grid.values())))

    def get_num_black_tiles(self) -> int:
        def is_odd(value):
            return value % 2 == 1
        return self.count_tiles_by_filter_function(is_odd)

    def get_num_white_tiles(self) -> int:
        def is_even(value):
            value % 2 == 0
        return self.count_tiles_by_filter_function(is_even)
    
    def get_coords_for_black_flip(self) -> List[Coord]:
        return []

    def get_coords_for_white_flip(self) -> List[Coord]:
        return []

    def flip(self, tiles_to_flip: List[Coord]):
        return

    def process(self):
        white_flip_list = self.get_coords_for_white_flip()
        black_flip_list = self.get_coords_for_black_flip()
        self.flip(white_flip_list + black_flip_list)
        print(f"After process: {self.get_num_black_tiles()}")


def parse_input(filename: str) -> List[List[Direction]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    list_of_lines = []
    for line in lines:
        directions = re.findall(r"(se|sw|nw|ne|e|w)", line)
        directions = list(map(lambda x: Direction[x], directions))
        list_of_lines.append(directions)
    return list_of_lines

crew_list = parse_input("input.txt")
board = Board()
for line in crew_list:
    coord = board.traverse_path_from_origin(line)
    board.ref_count_space(coord)
print(f"Part 1: {str(board.get_num_black_tiles())}")


