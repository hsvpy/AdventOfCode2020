from typing import List
from enum import Enum

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

def find_state(rows: List[List[State]], coord: (int, int)) -> State:
    row, column = coord
    current_state = rows[coord[1]][coord[0]]

    def coord_generator(row: int, column: int, row_length: int, col_length: int):
        for i in range(row - 1, row + 2):
            for j in range(column - 1, column + 2):
                if not (i==row and j==column) and i >= 0 and j >= 0 and i < row_length and j < col_length:                 
                    yield (i, j)

    if current_state == State.FLOOR:
        return State.FLOOR
    else:
        gen = coord_generator(row, column, len(rows[0]), len(rows))
        occupies = 0        
        for x, y in gen:            
            position = rows[y][x]
            if position == State.OCCUPIED:
                occupies += 1            
        if occupies == 0:
            return State.OCCUPIED
        elif occupies >= 4:
            return State.EMPTY
        else:
            return current_state

def run_rules(plane: List[List[State]]) -> List[List[State]]:
    return [[find_state(plane, (x,y)) for x, _ in enumerate(row)] for y, row in enumerate(plane)]


rows = parse_input('input.txt')
changed = True
sum_total = current_sum = 0
while changed:
    sum_total = current_sum
    rows = run_rules(rows)
    current_sum = sum([1 if (item == State.OCCUPIED) else 0 for row in rows for item in row])
    if(current_sum == sum_total):
        changed = False
print(f"Part 1: {current_sum}")