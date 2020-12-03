from typing import List
from functools import partial
from math import prod

def is_tree(char: str) -> bool:
    return '#' in char

def parse_input(filename: str) -> List[List[bool]]:
    with open(filename, 'r') as fh:
        rows_raw = fh.readlines()
    rows = list(map(lambda x: x.rstrip(), rows_raw))
    for index, row in enumerate(rows):
       rows[index] = list(map(is_tree, row)) 
    return rows

def calculate_next_index(x_step: int, y_step: int, cur_x: int, cur_y: int, row_length: int) -> (int, int):
    return ((cur_x + x_step) % row_length, cur_y + y_step)

def count_trees(x_step: int, y_step: int, rows: List[List[bool]]) -> int:
    row_length = len(rows[0])
    x = y = trees = 0
    next_partial = partial(calculate_next_index, x_step, y_step)
    while y < len(rows)-1:
        x, y = next_partial(x, y, row_length)
        if rows[y][x]:        
            trees += 1
    return trees


def part_1():
    rows = parse_input("input.txt")
    print(f"Part 1: {str(count_trees(3, 1, rows))}")

def part_2():
    rows = parse_input("input.txt")
    patterns = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    tree_totals = list(map(lambda coord: count_trees(coord[0], coord[1], rows), patterns))
    product = prod(tree_totals)
    print(f"Part 2: {str(product)}")


part_1()
part_2()
    
