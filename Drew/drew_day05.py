"""day 5: boarding passes"""
from typing import Tuple, List

TEST_INPUTS = {
    "FBFBBFFRLR": (44, 5, 357),
    "BFFFBBFRRR": (70, 7, 567),
    "FFFBBBFRRR": (14, 7, 119),
    "BBFFBBFRLL": (102, 4, 820),
}

with open("day05.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def boarding_pass_to_seat(boarding_pass: str) -> Tuple[int, int]:
    """Convert a boarding pass string into a row and column for seat finding

    Because the strings are just binary representations of integers, we can abuse
    Python's booleans and convert them from FBFBBFF to 0101100
    """
    binary_row = "".join(str(int(char == "B")) for char in boarding_pass[:7])
    binary_col = "".join(str(int(char == "R")) for char in boarding_pass[7:])
    row = int(binary_row, 2)
    col = int(binary_col, 2)
    return row, col


def seat_to_seat_id(seat: Tuple[int, int]) -> int:
    """Convert a row/column pair into a seat ID"""
    return seat[0] * 8 + seat[1]


def boarding_pass_to_seat_id(boarding_pass: str) -> int:
    """Convert a boarding pass string into seat ID

    Because the strings are just binary representations of integers, we can abuse
    Python's booleans and convert them from FBFBBFFRLR to 0101100101
    """
    seat_id = "".join(str(int(char in {"B", "R"})) for char in boarding_pass)

    return int(seat_id, 2)


def part_one(puzzle_input: List[str]) -> int:
    """Find the highest seat ID on the plane"""
    return max(boarding_pass_to_seat_id(line) for line in puzzle_input)


def part_two(puzzle_input: List[str]) -> int:
    """Find your seat: the boarding pass where there's a gap in the sequence"""
    seat_ids = sorted(boarding_pass_to_seat_id(line) for line in puzzle_input)
    for last_seat, current_seat in zip(
        seat_ids[:-1],
        seat_ids[1:],
    ):
        if current_seat != last_seat + 1:
            return last_seat + 1
    raise ValueError("no gap found")


def main():
    """here goes"""
    for boarding_pass, (row, col, seat_id) in TEST_INPUTS.items():
        assert boarding_pass_to_seat(boarding_pass) == (row, col), boarding_pass
        assert seat_to_seat_id((row, col)) == seat_id, boarding_pass
        assert boarding_pass_to_seat_id(boarding_pass) == seat_id, boarding_pass

    print(part_one(REAL_INPUT))
    print(part_two(REAL_INPUT))


if __name__ == "__main__":
    main()
