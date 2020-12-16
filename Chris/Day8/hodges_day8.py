import re
import sys
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
        new_instruction = Instruction(raw_instr, raw_arg)
        instructions.append(new_instruction)
    return instructions

def fix_instruction(ip: int, instructions: List[Instruction]) -> List[Instruction]:
    fixed_list = instructions.copy()
    if instructions[ip].opCode == "nop":
        fixed_list[ip].opCode = "jmp"
    elif instructions[ip].opCode == "jmp":
        fixed_list[ip].opCode = "nop"
    return fixed_list

def run_program(instructions: List[Instruction]) -> List[int]:
    ip = 0
    acc = 0
    visited = []
    while ip not in visited:
        if ip >= len(instructions):
            print(f"Part 2: {str(acc)}")
            return visited
        inst = instructions[ip]
        visited.append(ip)
        if inst.opCode == 'nop':
            ip += 1
        elif inst.opCode == 'acc':
            acc += inst.argument
            ip += 1
        elif inst.opCode == 'jmp':
            ip += inst.argument

    print(f"Part 1: {str(acc)}, {str(ip)}, {str(visited)}")
    return visited

instructions = parse_input('input.txt')
visited = run_program(instructions)
for ip in reversed(visited):
    run_program(fix_instruction(ip, instructions))
