"""day 17: 3D game of life"""
from typing import Dict, List, Tuple
from collections import defaultdict


TEST_INPUT = """.#.
..#
###""".splitlines()


with open("day17.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def next_state(
    coord: Tuple[int, int, int], grid: Dict[Tuple[int, int, int], bool]
) -> bool:
    """Apply rules in 3D space

    - If a coordinate is active and has 2 or 3 active neighbors, it stays active (off otherwise)
    - If a coordinate is inactive, it only activates if it has exactly 3 active neighbors
    """
    x, y, z = coord
    neighbors = [
        (x1, y1, z1)
        for x1 in [x + 1, x, x - 1]
        for y1 in [y + 1, y, y - 1]
        for z1 in [z + 1, z, z - 1]
        if (x1, y1, z1) != (x, y, z)
    ]
    active_neigbors = sum(grid[pos] for pos in neighbors)
    if grid[coord]:
        return active_neigbors in {2, 3}
    return active_neigbors == 3


def next_state_part_2(
    coord: Tuple[int, int, int, int], grid: Dict[Tuple[int, int, int], bool]
) -> bool:
    """Apply rules in 4D space

    - If a coordinate is active and has 2 or 3 active neighbors, it stays active (off otherwise)
    - If a coordinate is inactive, it only activates if it has exactly 3 active neighbors
    """
    x, y, z, w = coord
    neighbors = [
        (x1, y1, z1, w1)
        for x1 in [x + 1, x, x - 1]
        for y1 in [y + 1, y, y - 1]
        for z1 in [z + 1, z, z - 1]
        for w1 in [w + 1, w, w - 1]
        if (x1, y1, z1, w1) != (x, y, z, w)
    ]
    active_neigbors = sum(grid[pos] for pos in neighbors)
    if grid[coord]:
        return active_neigbors in {2, 3}
    return active_neigbors == 3


def parse_grid(
    puzzle_input: List[str], part_two: bool = False
) -> Dict[Tuple[int, int, int], bool]:
    """Convert the text grid into a 3D or 4D space"""
    grid = defaultdict(lambda: False)
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line.strip()):
            grid[(x, y, 0, 0) if part_two else (x, y, 0)] = char == "#"
    return grid


def part_one(puzzle_input: List[str], turns=6) -> bool:
    """Part 1: 3D space"""
    grid = parse_grid(puzzle_input)
    for _ in range(turns):
        sorted_by_x = sorted(grid)
        sorted_by_y = sorted(grid, key=lambda k: k[1])
        sorted_by_z = sorted(grid, key=lambda k: k[2])
        min_x = sorted_by_x[0][0] - 1
        max_x = sorted_by_x[-1][0] + 2
        min_y = sorted_by_y[0][1] - 1
        max_y = sorted_by_y[-1][1] + 2
        min_z = sorted_by_z[0][2] - 1
        max_z = sorted_by_z[-1][2] + 2
        new_grid = defaultdict(lambda: False)
        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    new_grid[(x, y, z)] = next_state((x, y, z), grid)
        grid = new_grid
    return sum(grid.values())


def part_two(puzzle_input: List[str], turns=6) -> bool:
    """Part 2: 4D space"""
    grid = parse_grid(puzzle_input, True)
    for _ in range(turns):
        sorted_by_x = sorted(grid)
        sorted_by_y = sorted(grid, key=lambda k: k[1])
        sorted_by_z = sorted(grid, key=lambda k: k[2])
        sorted_by_w = sorted(grid, key=lambda k: k[3])
        min_x = sorted_by_x[0][0] - 1
        max_x = sorted_by_x[-1][0] + 2
        min_y = sorted_by_y[0][1] - 1
        max_y = sorted_by_y[-1][1] + 2
        min_z = sorted_by_z[0][2] - 1
        max_z = sorted_by_z[-1][2] + 2
        min_w = sorted_by_w[0][3] - 1
        max_w = sorted_by_w[-1][3] + 2
        new_grid = defaultdict(lambda: False)
        for z in range(min_z, max_z):
            for y in range(min_y, max_y):
                for x in range(min_x, max_x):
                    for w in range(min_w, max_w):
                        new_grid[(x, y, z, w)] = next_state_part_2((x, y, z, w), grid)
        grid = new_grid
    return sum(grid.values())


assert part_one(TEST_INPUT) == 112, part_one(TEST_INPUT)
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 848, part_one(REAL_INPUT)
print(part_two(REAL_INPUT))
