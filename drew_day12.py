"""Day 12: navigation challenges"""
from typing import List, Tuple

TEST_INPUT = """F10
N3
F7
R90
F11""".splitlines()

with open("day12.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def follow_movements(instructions: List[str]) -> Tuple[int, int]:
    """Follow the movements as described in part 1"""
    start = 0j
    heading = 1
    for line in instructions:
        direction = line[0]
        amount = int(line[1:])
        if direction == "F":
            start += heading * amount
        elif direction == "N":
            start += 1j * amount
        elif direction == "S":
            start += -1j * amount
        elif direction == "E":
            start += amount
        elif direction == "W":
            start -= amount
        elif direction == "L":
            if amount not in {0, 90, 180, 270}:
                raise ValueError(f"unknown turn left amount {amount}")
            while amount > 0:
                heading *= 1j
                amount -= 90
        elif direction == "R":
            if amount not in {0, 90, 180, 270}:
                raise ValueError(f"unknown turn left amount {amount}")
            while amount > 0:
                heading *= -1j
                amount -= 90
        else:
            raise ValueError(f"unknown command {line}")
    return int(start.real), int(start.imag)


def follow_movements_part_two(instructions: List[str]) -> Tuple[int, int]:
    """Follow the movements in part two: everything moves the waypoint except F"""
    # for the sake of this puzzle, it was easier to copy and paste rather than handle a
    # bunch of conditionals
    start = 0j
    waypoint = 10 + 1j
    for line in instructions:
        direction = line[0]
        amount = int(line[1:])
        if direction == "F":
            start += waypoint * amount
        elif direction == "N":
            waypoint += 1j * amount
        elif direction == "S":
            waypoint += -1j * amount
        elif direction == "E":
            waypoint += amount
        elif direction == "W":
            waypoint -= amount
        elif direction == "L":
            if amount not in {0, 90, 180, 270}:
                # safety trap so I don't have to try to deal with trigonometry
                raise ValueError(f"unknown turn left amount {amount}")
            while amount > 0:
                waypoint *= 1j
                amount -= 90
        elif direction == "R":
            if amount not in {0, 90, 180, 270}:
                raise ValueError(f"unknown turn left amount {amount}")
            while amount > 0:
                waypoint *= -1j
                amount -= 90
        else:
            raise ValueError(f"unknown command {line}")
    return int(start.real), int(start.imag)


def part_one(puzzle_input: List[str]) -> int:
    """Part 1: exactly what it sounds like"""
    x, y = follow_movements(puzzle_input)
    return abs(x) + abs(y)


def part_two(puzzle_input: List[str]) -> int:
    """Part 2: here we go again"""
    x, y = follow_movements_part_two(puzzle_input)
    return abs(x) + abs(y)


def main():
    """command line start"""
    assert part_one(TEST_INPUT) == 25
    print(part_one(REAL_INPUT))
    assert part_two(TEST_INPUT) == 286
    print(part_two(REAL_INPUT))


if __name__ == "__main__":
    main()
