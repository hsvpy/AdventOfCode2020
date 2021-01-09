from typing import List
from functools import reduce

def parse_input(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        lines = list(map(lambda x: int(x), f.readlines()))
    return lines

def number_transform(num: int, sub_num:int) -> int:
    value = num * sub_num
    return value % 20201227

def find_loop_count(num: int, sub_num:int) -> int:
    loop_counter = 0
    accum = 1
    while accum != num:
        accum = number_transform(accum, sub_num)
        loop_counter += 1
    return loop_counter

sub_num = 7
keys = parse_input("input.txt")
loop_count = find_loop_count(keys[0], sub_num)
sub_num = keys[1]
accum = 1
for i in range(loop_count):
    accum = number_transform(accum, sub_num)
print(f"Part 1: {accum}")

