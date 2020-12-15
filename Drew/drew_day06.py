"""day 6: customs"""
from typing import List

TEST_INPUT = """abc

a
b
c

ab
ac

a
a
a
a

b""".splitlines()


with open("day06.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def part_one(puzzle_input: List[str]) -> int:
    """part one: sum of questions answered in each group"""
    score = 0
    active_group = set()
    for line in puzzle_input:
        if not line:
            score += len(active_group)
            active_group = set()
            continue
        active_group |= set(line)
    if active_group:
        score += len(active_group)
    return score


def part_two(puzzle_input: List[str]) -> int:
    """part 2: sum of questions *everyone* answered in a group"""
    score = 0
    active_group = set()
    # use this sentinel flag so we can set the first line to be
    # our comparison value
    new = True
    for line in puzzle_input:
        if not line:
            score += len(active_group)
            active_group = set()
            new = True
            continue
        if not new:
            active_group &= set(line)
        else:
            new = False
            active_group = set(line)
    if active_group:
        score += len(active_group)
    return score


assert part_one(TEST_INPUT) == 11
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 6
print(part_two(REAL_INPUT))
