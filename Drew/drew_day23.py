from collections import deque
from typing import Deque, List


TEST_INPUT = [int(i) for i in "389125467"]
REAL_INPUT = [int(i) for i in "318946572"]


def take_turn(cups: Deque[int]):
    max_cup = len(cups)
    current_cup = cups[0]
    cups.rotate(-1)
    drawn_cups = [cups.popleft() for _ in range(3)]
    destination = current_cup - 1
    if destination == 0:
        destination = max_cup
    while destination in drawn_cups:
        destination = destination - 1
        if destination == 0:
            destination = max_cup
    dest_index = cups.index(destination)
    cups.rotate(0 - dest_index - 1)
    for i in reversed(drawn_cups):
        cups.appendleft(i)
    new_target = cups.index(current_cup)
    cups.rotate(-new_target - 1)


def part_one(puzzle: List[int]) -> str:
    hand = deque(puzzle)
    for _ in range(100):
        take_turn(hand)
    finished = list(hand)
    start_index = finished.index(1)
    result = finished[start_index + 1 :] + finished[:start_index]
    return "".join(str(i) for i in result)


class Cup:
    def __init__(self, number: int) -> None:
        self.number = number
        self.next: Cup = None

    def __repr__(self):
        return str(self.number)


def part_two(puzzle: List[int]) -> int:
    cups: Dict[int, Cup] = {}
    for cup_number in puzzle:
        cups[cup_number] = Cup(cup_number)
    # tack on the extra numbers
    for cup_number in range(max(puzzle) + 1, int(1e6 + 1)):
        cups[cup_number] = Cup(cup_number)
    # build our relationships to the next one in the list
    for first, second in zip(puzzle, puzzle[1:] + [10]):
        cups[first].next = cups[second]
    # then tack on the rest
    for cup_number in range(10, 1000000):
        cups[cup_number].next = cups[cup_number + 1]
    # and finish the loop
    cups[1000000].next = cups[puzzle[0]]
    # coherence check
    for cup in cups.values():
        assert cup.next is not None, cup.number
    # and let us begin
    current_cup = cups[puzzle[0]]
    for turn in range(10000000):
        # draw 3
        removed_ids = [
            current_cup.next.number,
            current_cup.next.next.number,
            current_cup.next.next.next.number,
        ]
        # skip the three cups we've already pulled
        current_cup.next = current_cup.next.next.next.next
        destination_cup_id = current_cup.number - 1
        if destination_cup_id == 0:
            destination_cup_id = 1000000
        while destination_cup_id in removed_ids:
            destination_cup_id -= 1
            if destination_cup_id == 0:
                destination_cup_id = 1000000

        destination_cup = cups[destination_cup_id]
        # place the new ones
        cups[removed_ids[2]].next = destination_cup.next
        destination_cup.next = cups[removed_ids[0]]
        # and advance the turn
        current_cup = current_cup.next
    # done!
    return cups[1].next.number * cups[1].next.next.number


def main():
    test_hand = deque(TEST_INPUT)
    take_turn(test_hand)
    assert list(test_hand) == [2, 8, 9, 1, 5, 4, 6, 7, 3], test_hand
    take_turn(test_hand)
    assert list(test_hand) == [5, 4, 6, 7, 8, 9, 1, 3, 2], test_hand
    take_turn(test_hand)
    assert list(test_hand) == [8, 9, 1, 3, 4, 6, 7, 2, 5], test_hand
    test_result = part_one(TEST_INPUT)
    assert test_result == "67384529"
    print(part_one(REAL_INPUT))
    assert part_two(TEST_INPUT) == 149245887792
    print(part_two(REAL_INPUT))


if __name__ == "__main__":
    main()
