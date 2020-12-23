from typing import List
from enum import Enum
import operator

class State(Enum):
    FLOOR = 1
    EMPTY = 2
    OCCUPIED = 3

    def __repr__(self):
        if self.value == self.FLOOR.value:
            return '.'
        elif self.value == self.OCCUPIED.value:
            return '#'
        else:
            return 'L'

class Direction(Enum):
    UP = (0, 1)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP_LEFT = (-1, 1)
    UP_RIGHT = (1, 1)
    DOWN_LEFT = (-1, -1)
    DOWN_RIGHT = (1, -1)
   
def from_char(char) -> State:
    mapping = {
        '.': State.FLOOR,
        'L': State.EMPTY,
        '#': State.OCCUPIED
    }
    return mapping[char]


def parse_input(filename: str) -> List[List[State]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    return_list = []
    for row in lines:
        return_list.append([from_char(char) for char in row.rstrip('\n')])
    return return_list

def find_state(rows: List[List[State]], coord: (int, int), part2: bool) -> State:
    row, column = coord
    current_state = rows[coord[1]][coord[0]]

    def valid(i: int, j: int, row_length: int, col_length: int) -> bool:
        return not (i==row and j==column) and i >= 0 and j >= 0 and i < row_length and j < col_length

    def coord_generator(row: int, column: int, row_length: int, col_length: int):
        for i in range(row - 1, row + 2):
            for j in range(column - 1, column + 2):
                if valid(i, j, row_length, col_length):                 
                    yield (i, j)

    def vector_coord_gen(row: int, column: int, row_length: int, col_length: int):
        for d in Direction:
            current_coord = (row, column)
            next_coord = tuple(map(operator.add, d.value, current_coord))       
            while valid(next_coord[0], next_coord[1], row_length, col_length):            
                if(rows[next_coord[1]][next_coord[0]] != State.FLOOR):
                    yield (next_coord[0], next_coord[1])
                    break
                current_coord = next_coord
                next_coord = tuple(map(operator.add, d.value, current_coord))
                        

    if current_state == State.FLOOR:
        return State.FLOOR
    else:
        gen = coord_generator(row, column, len(rows[0]), len(rows)) if not part2 else \
                vector_coord_gen(row, column, len(rows[0]), len(rows))
        occupies = 0        
        for x, y in gen:            
            position = rows[y][x]
            if position == State.OCCUPIED:
                occupies += 1            
        if occupies == 0:
            return State.OCCUPIED
        elif not part2 and occupies >= 4:
            return State.EMPTY
        elif part2 and occupies >= 5:
            return State.EMPTY        
        else:
            return current_state

def run_rules(plane: List[List[State]], part2: bool) -> List[List[State]]:
    return [[find_state(plane, (x,y), part2) for x, _ in enumerate(row)] for y, row in enumerate(plane)]


def get_occupied_seats(part2: bool) -> int:
    rows = parse_input('input.txt')
    changed = True
    sum_total = current_sum = 0
    while changed:
        sum_total = current_sum
        rows = run_rules(rows, part2)
        current_sum = sum([1 if (item == State.OCCUPIED) else 0 for row in rows for item in row])
        if(current_sum == sum_total):
            changed = False
    return current_sum
print(f"Part 1: {get_occupied_seats(False)}")
print(f"Part 2: {get_occupied_seats(True)}")