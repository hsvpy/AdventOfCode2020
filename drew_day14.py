"""Day 14: memory msking"""
from collections import defaultdict
from typing import Dict, List

with open("day14.txt") as infile:
    REAL_INPUT = [line.strip().split(" = ") for line in infile]


TEST_INPUT = [
    line.split(" = ")
    for line in """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
""".splitlines()
]

PART_TWO_TEST_INPUT = [
    line.split(" = ")
    for line in """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1""".splitlines()
]


def apply_one(value: int, bit_value: int) -> int:
    bitmask = 1 << bit_value
    return value | bitmask


def apply_zero(value: int, bit_value: int, length: int) -> int:
    bitmask = 2 ** length - 1
    # use xor to turn off just the one bit
    bitmask ^= 1 << bit_value
    return value & bitmask


def possible_addresses(mask: str, write_value: int) -> List[int]:
    result = [write_value]
    for index, value in enumerate(mask):
        bit_value = len(mask) - index - 1
        if value == "X":
            new_result = []
            for number in result:
                new_result += [
                    apply_one(number, bit_value),
                    apply_zero(number, bit_value, len(mask)),
                ]
        else:
            value = int(value)
            if value:
                new_result = [apply_one(number, bit_value) for number in result]
            else:
                # zero is a no-op
                continue
        result = new_result
    return result


def apply_mask(mask: str, write_value: int) -> int:
    for index, value in enumerate(mask):
        bit_value = len(mask) - index - 1
        if value == "X":
            continue
        value = int(value)
        if value:
            bitmask = value << bit_value
            write_value |= bitmask
        else:
            bitmask = 2 ** len(mask) - 1
            # use xor to turn off just the one bit
            bitmask ^= 1 << bit_value
            write_value &= bitmask
    return write_value


def parse_command(
    cmd: str,
    value: str,
    active_mask: str,
    memory: Dict[int, int],
    part_two: bool = False,
) -> str:
    if cmd == "mask":
        active_mask = value
    elif cmd.startswith("mem"):
        addr = int("".join(i for i in cmd if i.isdigit()))
        if part_two:
            addresses = possible_addresses(active_mask, addr)
            for addr in addresses:
                memory[addr] = int(value)
        else:
            memory[addr] = apply_mask(active_mask, int(value))
    else:
        raise ValueError(f"Unknown cmd {cmd} {value}")
    return active_mask


def run(puzzle_input: List[List[str]], part_two: bool = False) -> int:
    memory = defaultdict(lambda: 0)
    active_mask = "X" * 36
    for cmd, value in puzzle_input:
        active_mask = parse_command(cmd, value, active_mask, memory, part_two)
    return sum(memory.values())


def test_masks():
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert apply_mask(mask, 0) == 64, apply_mask(mask, 0)
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert apply_mask(mask, 11) == 73
    mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X"
    assert apply_mask(mask, 101) == 101
    mask = "000000000000000000000000000000X1001X"
    assert sorted(possible_addresses(mask, 42)) == [26, 27, 58, 59]


if __name__ == "__main__":
    test_masks()
    assert run(TEST_INPUT) == 165, run(TEST_INPUT)
    print(run(puzzle_input=REAL_INPUT))
    assert run(PART_TWO_TEST_INPUT, True) == 208
    print(run(puzzle_input=REAL_INPUT, part_two=True))
