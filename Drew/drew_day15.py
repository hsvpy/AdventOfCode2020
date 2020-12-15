"""Day 15: memory game"""

from typing import Dict, List


TEST_INPUTS = {
    "0,3,6": 436,
    "1,3,2": 1,
    "2,1,3": 10,
    "2,3,1": 78,
    "1,2,3": 27,
    "3,2,1": 438,
    "3,1,2": 1836,
}


class Game:
    def __init__(self, numbers: str) -> None:
        super().__init__()
        self.turns: Dict[int, List[int]] = {}
        self.next_turn_number = 1
        self.last_number_spoken = 0
        for number_str in numbers.split(","):
            number = int(number_str)
            if number in self.turns:
                self.turns[number] = (self.turns[number] + [self.next_turn_number])[-2:]
            else:
                self.turns[number] = [self.next_turn_number]
            self.last_number_spoken = number
            self.next_turn_number += 1

    def take_turn(self):
        # print(self.turns, self.last_number_spoken)
        try:
            previous_turns = self.turns[self.last_number_spoken]
        except KeyError:
            print("oop")
            self.turns[self.last_number_spoken] = [self.next_turn_number]
            self.last_number_spoken = 0
            self.next_turn_number += 1
            return
        # print(previous_turns)
        if len(previous_turns) < 2:
            self.last_number_spoken = 0
        else:
            first, second = previous_turns
            self.last_number_spoken = second - first

        self.turns[self.last_number_spoken] = (
            self.turns.get(self.last_number_spoken, []) + [self.next_turn_number]
        )[-2:]
        self.next_turn_number += 1


def part_one(puzzle_input: str, turns=2020) -> int:
    game = Game(puzzle_input)
    while game.next_turn_number <= turns:
        game.take_turn()
        # print(game.next_turn_number, game.last_number_spoken)
    return game.last_number_spoken


def main():
    for numbers, target in TEST_INPUTS.items():
        assert part_one(numbers) == target, part_one(numbers)
    real_input = "17,1,3,16,19,0"
    print(part_one(real_input))
    print(part_one(real_input, 30000000))


if __name__ == "__main__":
    main()
