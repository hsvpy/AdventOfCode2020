import re
from enum import Enum
from typing import List, Dict
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

    def get_neighbors(self):
        return [self.neighbor(direction) for direction in Direction]


class Board(object):
    def __init__(self):
        self.grid = {}
    
    def ref_count_space(self, coord: Coord):
        if coord in self.grid:
            self.grid[coord] += 1
        else:
            self.grid[coord] = 1

    @staticmethod
    def traverse_path_from_origin(directions: List[Direction]) -> Coord:
        coord = Coord(0, 0, 0)
        for direction in directions:
            coord = coord.neighbor(direction)
        return coord

    @staticmethod
    def is_odd(value):
        return value % 2 == 1

    @staticmethod
    def is_even(value):
        value % 2 == 0

    def count_tiles_by_filter_function(self, fn, tiles=None) -> int:
        if not tiles:
            tiles = self.grid.values()
        return len(list(filter(fn, tiles)))

    def get_tiles_by_filter_function(self, fn) -> Dict[Coord, int]:
        return dict(filter(lambda x: fn(x[1]), self.grid.items()))

    def get_num_black_tiles(self, tiles=None) -> int:
        return self.count_tiles_by_filter_function(Board.is_odd, tiles)

    def tile_is_black(self, coord: Coord) -> bool:
        return coord in self.grid and Board.is_odd(self.grid[coord])
    
    def get_coords_for_flip(self) -> List[Coord]:
        def get_number_black_neighbors(tiles: List[Coord]) -> int:
            return sum([self.tile_is_black(neighbor) for neighbor in tiles])

        def black_needs_flip(black_neighbor_count: int) -> bool:
            return True if black_neighbor_count == 0 or black_neighbor_count > 2 else False

        def white_needs_flip(black_neighbor_count: int) -> bool:
            return True if black_neighbor_count == 2 else False
        black_tiles = self.get_tiles_by_filter_function(Board.is_odd).keys()
        black_tiles_with_neighbors = list(zip(black_tiles, [tile.get_neighbors() for tile in black_tiles]))
        black_flip_values = set(dict(filter(lambda x: black_needs_flip(get_number_black_neighbors(x[1])), black_tiles_with_neighbors)).keys())
        white_flip_values = set()
        for black_tile in black_tiles_with_neighbors:
            for neighbor in black_tile[1]:
                if not self.tile_is_black(neighbor):
                    if white_needs_flip(get_number_black_neighbors(neighbor.get_neighbors())):
                        white_flip_values.add(neighbor)

        all_flips = black_flip_values.union(white_flip_values)
        return all_flips

    def flip(self, tiles_to_flip: List[Coord]):
        for tile in tiles_to_flip:
            self.ref_count_space(tile)
        return

    def process(self):
        flip_list = self.get_coords_for_flip()
        self.flip(flip_list)


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
    coord = Board.traverse_path_from_origin(line)
    board.ref_count_space(coord)
print(f"Part 1: {str(board.get_num_black_tiles())}")
for i in range(100):
    board.process()
print(f"Part 2: {str(board.get_num_black_tiles())}")
