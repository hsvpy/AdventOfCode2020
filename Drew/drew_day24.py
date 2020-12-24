"""Day 24: Lobby layout

Coordinate system taken from
https://www.redblobgames.com/grids/hexagons/#coordinates
"""

from collections import defaultdict
from day23 import REAL_INPUT
from typing import Dict, List, Tuple


MOVES = {
    "e": [1, -1, 0],
    "w": [-1, 1, 0],
    "se": [0, -1, 1],
    "sw": [-1, 0, 1],
    "nw": [0, 1, -1],
    "ne": [1, 0, -1],
}

TEST_INPUT = """sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".splitlines()


EXPECTED_PART_TWO_RESULTS = {
    2: 12,
    3: 25,
    4: 14,
    5: 23,
    6: 28,
    7: 41,
    8: 37,
    9: 49,
    10: 37,
    20: 132,
    30: 259,
    40: 406,
    50: 566,
    60: 788,
    70: 1106,
    80: 1373,
    90: 1844,
    100: 2208,
}

with open("day24.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def parse_step(line: str) -> Tuple[int, int, int]:
    """Follow a step from start to finish"""
    index = 0
    start = (0, 0, 0)
    while index < len(line):
        if line[index] in MOVES:
            x, y, z = start
            x1, y1, z1 = MOVES[line[index]]
            start = (x + x1, y + y1, z + z1)
            index += 1
        elif line[index : index + 2] in MOVES:
            x, y, z = start
            x1, y1, z1 = MOVES[line[index : index + 2]]
            start = (x + x1, y + y1, z + z1)
            index += 2
        else:
            raise ValueError(f"Unknown step {line[index:index + 2]}")
    return start


def part_one(puzzle: List[str]) -> int:
    grid: Dict[Tuple[int], bool] = defaultdict(lambda: False)
    for line in puzzle:
        coordinates = parse_step(line)
        grid[coordinates] = not grid[coordinates]
    return sum(grid.values())


def get_neighbor_coordinates(pos: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    result = []
    x, y, z = pos
    for x1, y1, z1 in MOVES.values():
        result.append((x + x1, y + y1, z + z1))
    return result


def next_state(
    pos: Tuple[int, int, int], grid: Dict[Tuple[int, int, int], bool]
) -> bool:
    neighbors = get_neighbor_coordinates(pos)
    active_neighbors = sum(grid[neighbor] for neighbor in neighbors)
    state = grid[pos]
    if state:
        if active_neighbors not in {1, 2}:
            # if the tile is black and there are 0 or more than two active neighbors,
            # flip it
            state = False
    else:
        if active_neighbors == 2:
            # if it's white and there are exactly two black tiles next to it, flip it
            state = True
    return state


def take_turn(
    grid: Dict[Tuple[int, int, int], bool]
) -> Dict[Tuple[int, int, int], bool]:
    x_values = sorted(grid)
    y_values = sorted(grid, key=lambda k: k[1])
    z_values = sorted(grid, key=lambda k: k[2])
    min_x = x_values[0][0] - 1
    max_x = x_values[-1][0] + 2
    min_y = y_values[0][1] - 1
    max_y = y_values[-1][1] + 2
    min_z = z_values[0][2] - 1
    max_z = z_values[-1][2] + 2
    new_grid = defaultdict(lambda: False)
    new_grid.update(
        {
            (x, y, z): next_state((x, y, z), grid)
            for x in range(min_x, max_x)
            for y in range(min_y, max_y)
            for z in range(min_z, max_z)
            # this conditional is crucial
            if x + y + z == 0
        }
    )
    return new_grid


def part_two(puzzle: List[str], days: int = 100) -> int:
    grid: Dict[Tuple[int], bool] = defaultdict(lambda: False)
    for line in puzzle:
        coordinates = parse_step(line)
        grid[coordinates] = not grid[coordinates]
    testing = puzzle == TEST_INPUT
    for day in range(days):
        grid = take_turn(grid)
        if testing:
            try:
                expected_result = EXPECTED_PART_TWO_RESULTS[day + 1]
            except KeyError:
                pass
            else:
                assert expected_result == sum(grid.values()), (
                    day + 1,
                    sum(grid.values()),
                    grid,
                )
        if not day % 10:
            # this code gets slower as the days go on
            print(f"in progress: day {day}")
    return sum(grid.values())


def main():
    assert part_one(TEST_INPUT) == 10, part_one(TEST_INPUT)
    print("part 1 result:", part_one(REAL_INPUT))
    assert part_two(TEST_INPUT) == 2208, part_two(TEST_INPUT)
    print("part 2 result", part_two(REAL_INPUT))


if __name__ == "__main__":
    main()
