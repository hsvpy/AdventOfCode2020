import re
from typing import List
from enum import Enum, auto

class Instruction:     
    def __init__(self, opCode: str, arg: str):
        self.opCode: str = opCode
        self.argument: int = int(arg)
    
    def __repr__(self):
        print(f'{str(self.opCode)} {self.argument}')

def parse_input(filename: str) -> List[Instruction]:
    with open(filename, 'r') as f:
        raw_instructions = f.readlines()
    instructions = []
    for line in raw_instructions:
        matches = re.search(r'^(nop|acc|jmp) (.*)$', line)
        raw_instr, raw_arg = matches.group(1), matches.group(2)
        instructions.append([Instruction(raw_instr, raw_arg)])
    return instructions

instructions = parse_input('test.txt')
print(str(instructions))