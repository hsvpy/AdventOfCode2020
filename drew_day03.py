from typing import List, Set, Tuple


TEST_INPUT = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".splitlines()


with open("day03.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def parse_input(text: List[str]) -> Set[Tuple[int, int]]:
    grid = set()
    for y, row in enumerate(text):
        for x, char in enumerate(row):
            if char == "#":
                grid.add((x, y))
    return grid


def part_one(puzzle_input: List[str], x_slope: int = 3, y_slope: int = 1) -> int:
    target_y = len(puzzle_input)
    width = len(puzzle_input[0])
    grid = parse_input(puzzle_input)
    x, y = 0, 0
    trees_hit = 0
    while y < target_y:
        trees_hit += (x % width, y) in grid
        y += y_slope
        x += x_slope
    return trees_hit


def part_two(puzzle_input: List[str]) -> int:
    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    total = 1
    for x_slope, y_slope in slopes:
        total *= part_one(puzzle_input, x_slope, y_slope)
    return total


assert part_one(TEST_INPUT) == 7
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 336
print(part_two(REAL_INPUT))
