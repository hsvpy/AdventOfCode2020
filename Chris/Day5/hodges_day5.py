import re
from typing import List

def convert_row(row: str) -> int:
    return(int(row.replace('F', '0').replace('B', '1'), 2))

def convert_column(column: str) -> int:
    return(int(column.replace('L', '0').replace('R', '1'), 2))



def parse_input(filename: str) -> List[int]:
    with open(filename, 'r') as fh:
        passes = fh.readlines()
    seat_ids = []
    for pass_raw in passes:
        if match := re.search(r'([BF]{7})([LR]{3})', pass_raw):
            seat_ids.append(convert_row(match.group(1)) * 8 + convert_column(match.group(2)))
    return seat_ids

def find_gap(seats: List[int]) -> int:
    for seat in range(0, len(seats) - 1):
        if seats[seat+1] - seats[seat] > 1:
            return seats[seat] + 1
    return -1

seat_ids = sorted(parse_input('input.txt'))
print(f'Part 1: {seat_ids[-1]}')
print(f'Part 2: {str(find_gap(seat_ids))}')
print(str(sorted(seat_ids)))