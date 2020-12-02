from typing import List


TEST_INPUT = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc""".splitlines()

with open("day02.txt") as infile:
    REAL_INPUT = [line for line in infile]


def valid_password_count(text: List[str]) -> int:
    valid_count = 0
    for line in text:
        char_count, char_block, pw = line.split(" ")
        min, max = [int(i) for i in char_count.split("-")]
        validation_char = char_block[0]
        valid = pw.count(validation_char) in range(min, max + 1)
        valid_count += int(valid)
    return valid_count


def part_two(text: List[str]) -> int:
    valid_count = 0
    for line in text:
        positions, char_block, pw = line.split(" ")
        left, right = [int(i) - 1 for i in positions.split("-")]
        validation_char = char_block[0]
        # cheat and use a bitwise xor since True and False are
        # subclasses ints with value 1 and 0
        valid = (pw[left] == validation_char) ^ (pw[right] == validation_char)
        valid_count += int(valid)
    return valid_count


assert valid_password_count(TEST_INPUT) == 2
print(valid_password_count(REAL_INPUT))
assert part_two(TEST_INPUT) == 1
print(part_two(REAL_INPUT))
