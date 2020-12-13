"""Day 13: shutle search"""
from typing import List, Tuple
from functools import reduce

RAW_TEST_INPUT = """939
7,13,x,x,59,x,31,19"""
EARLIEST_TIMESTAMP = int(RAW_TEST_INPUT.split()[0])
IDS = [int(i) for i in RAW_TEST_INPUT.split()[1].split(",") if i != "x"]
PART_TWO_TEST_INPUT = [
    (index, int(i))
    for index, i in enumerate(RAW_TEST_INPUT.split()[1].split(","))
    if i != "x"
]

with open("day13.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]
    REAL_TIMESTAMP = int(REAL_INPUT[0])
    REAL_IDS = [int(i) for i in REAL_INPUT[1].split(",") if i != "x"]
    PART_TWO_IDS = [
        (index, int(i)) for index, i in enumerate(REAL_INPUT[1].split(",")) if i != "x"
    ]


def part_one(earliest_timestamp: int, ids: List[int]) -> int:
    earliest_arrivals = [(i * ((earliest_timestamp // i) + 1), i) for i in ids]
    earliest, pk = min(earliest_arrivals)

    return (earliest - earliest_timestamp) * pk


def chinese_remainder(n: int, a: int) -> int:
    """Chinese remainder theorem in Python

    shamelessly stolen from
    https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
    """
    sum = 0
    prod = reduce(lambda a, b: a * b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


def part_two(delta_t_and_ids: List[Tuple[int, int]]) -> int:
    """solve part two using the Chinese Remainder Theorem:

    so the test input looks like

    t ≡  0 (mod 7)
    t ≡ -1 (mod 13)
    t ≡ -4 (mod 59)
    t ≡ -6 (mod 31)
    t ≡ -7 (mod 19)
    """

    n_s = [0 - i[0] for i in delta_t_and_ids]
    a_s = [i[1] for i in delta_t_and_ids]
    return chinese_remainder(a_s, n_s)


assert part_one(EARLIEST_TIMESTAMP, IDS) == 295
print(part_one(REAL_TIMESTAMP, REAL_IDS))
assert part_two(PART_TWO_TEST_INPUT) == 1068781
print(part_two(PART_TWO_IDS))
