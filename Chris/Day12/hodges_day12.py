from typing import List, Tuple
from enum import Enum
import re
import operator

class Direction(Enum):
    N = (0, 1)
    S = (0, -1)
    E = (1, 0)
    W = (-1, 0)

turn_right = {
    Direction.N: Direction.E,
    Direction.E: Direction.S,
    Direction.S: Direction.W,
    Direction.W: Direction.N
}

turn_left = {
    Direction.N: Direction.W,
    Direction.W: Direction.S,
    Direction.S: Direction.E,
    Direction.E: Direction.N
}

degrees_to_direction = {
    0: Direction.N,
    90: Direction.E,
    180: Direction.S,
    270: Direction.W,
}

direction_to_degrees = {
    Direction.N: 0,
    Direction.E: 90,
    Direction.S: 180,
    Direction.W: 270
}

def parse_input(filename: str) -> List[Tuple[str, int]]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    lines = list(map(lambda line: line.rstrip('\n'), lines))
    records = []
    for entry in lines:
        match = re.search(r"^(\w)(\d+)$", entry)
        if match:
            records.append((match.group(1), int(match.group(2))))
    return records

def convert_left_right(current_direction: Direction, degrees: int, is_left: bool) -> Direction:
    multiplier = -1 if is_left else 1
    current_degrees = direction_to_degrees[current_direction]
    new_degrees = (current_degrees + degrees*multiplier) % 360
    return degrees_to_direction[new_degrees]

def move(current_position: Tuple[int, int], direction: Direction, magnitude: int) -> Tuple[int, int]:
    commanded_move = tuple(map(operator.mul, direction.value, (magnitude, magnitude)))
    return tuple(map(operator.add, current_position, commanded_move))


def manhattan_distance(coord: Tuple[int, int]):
    return sum(tuple(map(lambda x: abs(x), coord)))

def run_steps(steps: List[Tuple[str, int]]) -> Tuple[Direction, Tuple[int, int]]:
    current_heading = Direction.E
    current_position = (0, 0)
    for step in steps:
        instruction, value = step
        if instruction in Direction.__members__:
            current_position = move(current_position, Direction[instruction], value)
        elif instruction in ('L', 'R'):
            current_heading = convert_left_right(current_heading, value, instruction == 'L')            
        elif instruction in ('F'):
            current_position = move(current_position, current_heading, value)
    return (current_heading, current_position)


instr = parse_input('input.txt')
heading, coord = run_steps(instr)
print(f"Part 1: {manhattan_distance(coord)}")
