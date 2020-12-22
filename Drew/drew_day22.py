from typing import Deque, List, Set, Tuple
from collections import deque


TEST_INPUT = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".split(
    "\n\n"
)

with open("day22.txt") as infile:
    REAL_INPUT = infile.read().split("\n\n")


def build_hands(puzzle_input: List[str]) -> List[Deque[int]]:
    result = []
    for hand_desc in puzzle_input:
        result.append(
            deque(
                list(
                    int(i) for hand in hand_desc.splitlines()[1:] for i in hand.split()
                )
            )
        )
    return result


class GameOver(Exception):
    pass


def play_round(hands: List[Deque[int]], part_two: bool = False):
    try:
        p1_card = hands[0].popleft()
    except IndexError as exc:
        raise GameOver() from exc
    try:
        p2_card = hands[1].popleft()
    except IndexError as exc:
        # put the player 1 card back in the deck
        hands[0].appendleft(p1_card)
        raise GameOver() from exc
    if part_two:
        if len(hands[0]) >= p1_card and len(hands[1]) >= p2_card:
            new_hands = [
                deque(list(hands[0])[:p1_card]),
                deque(list(hands[1])[:p2_card]),
            ]
            winner_score = play_game(new_hands, True)
            if winner_score == score_hand(new_hands[0]):
                hands[0].append(p1_card)
                hands[0].append(p2_card)
            elif winner_score == score_hand(new_hands[1]):
                hands[1].append(p2_card)
                hands[1].append(p1_card)
            else:
                raise ValueError("unknown winner score")
            return
    if p1_card > p2_card:
        hands[0].append(p1_card)
        hands[0].append(p2_card)
    elif p2_card > p1_card:
        hands[1].append(p2_card)
        hands[1].append(p1_card)
    else:
        raise ValueError("same card should not be possible")


def score_hand(hand: Deque[int]) -> int:
    hand_length = len(hand)
    return sum(value * (hand_length - index) for index, value in enumerate(hand))


def part_one(puzzle_input: List[str], part_two: bool = False) -> int:
    hands = build_hands(puzzle_input)
    return play_game(hands, part_two)


def play_game(hands: List[Deque[int]], part_two: bool = False) -> int:
    turns = 0
    hands_seen: Set[Tuple[Tuple[int]]] = set()
    while True:
        if part_two:
            active_hands = tuple(tuple(i) for i in hands)
            if active_hands in hands_seen:
                return score_hand(hands[0])
            hands_seen.add(active_hands)
        try:
            play_round(hands, part_two=part_two)
        except GameOver:
            scores = [score_hand(hand) for hand in hands]
            assert (scores[0] == 0) is not (scores[1] == 0)
            return [i for i in scores if i != 0][0]
        else:
            turns += 1


def main():
    p1_score = part_one(TEST_INPUT)
    assert p1_score == 306, p1_score
    print(part_one(REAL_INPUT))
    p2_score = part_one(TEST_INPUT, True)
    assert p2_score == 291, p2_score
    print(part_one(REAL_INPUT, True))


if __name__ == "__main__":
    main()
