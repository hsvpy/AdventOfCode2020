"""Day 8: oh no not a CPU again"""
from typing import List, Union


TEST_INPUT = """nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6""".splitlines()

TEST_ANSWER = 5


with open("day08.txt") as infile:
    REAL_INPUT = [line for line in infile]


class CPU:
    """Basic CPU: one register and an instruction pointer"""

    def __init__(self, instructions: str):
        self.instructions = instructions
        self.instruction_pointer = 0
        self.accumulator = 0

    def nop(self, arg: str):
        self.instruction_pointer += 1

    def parse_arg(self, arg: str) -> int:
        return int(arg.replace("+", ""))

    def acc(self, arg: str):
        self.accumulator += self.parse_arg(arg)
        self.instruction_pointer += 1

    def jmp(self, arg: str):
        self.instruction_pointer += self.parse_arg(arg)

    def next(self):
        funcs = {
            "acc": self.acc,
            "jmp": self.jmp,
            "nop": self.nop,
        }
        try:
            func, arg = self.instructions[self.instruction_pointer].split()
        except IndexError:
            raise ProgramTerminated(self)
        funcs[func](arg)


class ProgramTerminated(Exception):
    def __init__(self, cpu: CPU, *args: object) -> None:
        self.cpu = cpu
        msg = f"Program terminated; instruction ptr {cpu.instruction_pointer}"
        super().__init__(msg, *args)


def part_one(puzzle_input: List[str]) -> int:
    """Part one: run until the program loops, then return the accumulator"""
    cpu = CPU(puzzle_input)
    instructions_seen = set()
    while cpu.instruction_pointer not in instructions_seen:
        instructions_seen.add(cpu.instruction_pointer)
        cpu.next()
    return cpu.accumulator


def part_two(puzzle_input: List[str]) -> int:
    """Part two: find which instruction we need to toggle from jmp to nop or vice versa

    This will force the program to exit normally"""
    for index in range(len(puzzle_input)):
        instruction, arg = puzzle_input[index].split()
        if instruction == "acc":
            # can't change accumulates
            continue
        if instruction == "jmp":
            new_instr = "nop"
        else:
            new_instr = "jmp"
        puzzle_input[index] = f"{new_instr} {arg}"
        try:
            part_one(puzzle_input)
        except ProgramTerminated as exc:
            # Yay!
            return exc.cpu.accumulator
        # oh well. Reset the instruction and try again
        puzzle_input[index] = f"{instruction} {arg}"
    raise ValueError("nothing worked")


assert part_one(TEST_INPUT) == TEST_ANSWER
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 8
print(part_two(REAL_INPUT))
