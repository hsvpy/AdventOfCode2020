#!/usr/bin/env python

from typing import List


TEST_INPUT = [
    int(i)
    for i in """1721
979
366
299
675
1456""".splitlines()
]

TARGET = 2020

with open("day01.txt") as infile:
    REAL_INPUT = [int(i) for i in infile]


def part_one(input_list: List[str]) -> int:
    set_input = set(input_list)
    for i in set_input:
        if TARGET - i in set_input:
            return i * (TARGET - i)


def part_two(input_list: List[str]) -> int:
    set_input = set(input_list)
    for i in set_input:
        for j in set_input:
            if TARGET - i - j in set_input and i != j:
                return i * (TARGET - i - j) * j


assert part_one(TEST_INPUT) == 514579
assert part_two(TEST_INPUT) == 241861950
print(part_one(REAL_INPUT))
print(part_two(REAL_INPUT))
