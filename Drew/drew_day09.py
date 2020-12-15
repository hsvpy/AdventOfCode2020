"""day 9: encoding"""

from typing import List


PREAMBLE_LENGTH = 25


TEST_INPUT = [
    int(i)
    for i in """35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576""".split()
]

with open("day09.txt") as infile:
    REAL_INPUT = [int(i.strip()) for i in infile]


def is_valid_number(number: int, numbers_seen: List[int], search_window: int) -> bool:
    valid_candidates = set(numbers_seen[-search_window:])

    for candidate in valid_candidates:
        alternate_candidate = number - candidate
        if alternate_candidate != candidate and alternate_candidate in valid_candidates:
            return True
    return False


def part_one(puzzle_input: List[int], search_window=PREAMBLE_LENGTH) -> int:
    numbers_seen = []
    for index, number in enumerate(puzzle_input):
        if index >= search_window:
            if not is_valid_number(number, numbers_seen, search_window):
                return number
        numbers_seen.append(number)


def part_two(puzzle_input: List[int], part_one_result: int) -> int:
    for index, number in enumerate(puzzle_input):
        numbers_seen = [number]
        for next_number in puzzle_input[index + 1 :]:
            numbers_seen.append(next_number)
            running_total = sum(numbers_seen)
            if running_total == part_one_result:
                return min(numbers_seen) + max(numbers_seen)
            elif running_total > part_one_result:
                break
    raise ValueError("did not work")


assert part_one(TEST_INPUT, 5) == 127
PART_ONE_RESULT = part_one(REAL_INPUT)
print(PART_ONE_RESULT)
assert part_two(TEST_INPUT, 127) == 62
print(part_two(REAL_INPUT, PART_ONE_RESULT))
