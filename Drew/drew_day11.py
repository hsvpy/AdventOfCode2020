"""day 11: the game of chairs"""

from typing import Dict


TEST_INPUT = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""

with open("day11.txt") as infile:
    REAL_INPUT = infile.read()


class Grid:
    def __init__(self, grid: str, part_two: bool = False) -> None:
        super().__init__()
        self.grid = self.parse_grid(grid)
        self.part_two = part_two
        self.max_real = max(int(i.real) for i in self.grid)
        self.min_imag = min(int(i.imag) for i in self.grid)
        self.min_real = self.max_imag = 0

    def parse_grid(self, grid: str) -> Dict[complex, bool]:
        result = {}
        for y, row in enumerate(grid.splitlines()):
            for x, char in enumerate(row.strip()):
                if char == ".":
                    # empty floor
                    continue
                result[x - (1j * y)] = char == "#"
        return result

    def adjacent_neighbors(self, pos: complex):
        if not self.part_two:
            return sum(
                self.grid.get(coord, False)
                for coord in [
                    pos + 1,
                    pos - 1,
                    pos + 1j,
                    pos - 1j,
                    pos + 1j + 1,
                    pos + 1j - 1,
                    pos - 1j + 1,
                    pos - 1j - 1,
                ]
            )
        vectors = [
            1,  # right
            -1,  # left
            1 + 1j,  # up and right
            1 - 1j,  # down and right
            -1 + 1j,  # up and left
            -1 - 1j,  # down and left
            1j,  # up
            -1j,  # down
        ]
        neighbors_found = 0

        for vec in vectors:
            new_pos = pos
            while (
                new_pos.real >= self.min_real
                and new_pos.real <= self.max_real
                and new_pos.imag >= self.min_imag
                and new_pos.imag <= self.max_imag
            ):
                new_pos += vec
                if self.grid.get(new_pos) is not None:
                    neighbors_found += self.grid[new_pos]
                    break
        return neighbors_found

    def next_state(self, pos: complex) -> bool:
        neighbors = self.adjacent_neighbors(pos)
        if neighbors >= (5 if self.part_two else 4):
            return False
        if neighbors == 0:
            return True
        return self.grid[pos]

    def run_until_loop(self) -> int:
        iterations = 0
        while True:
            iterations += 1
            new_grid = {pos: self.next_state(pos) for pos in self.grid}
            if new_grid == self.grid:
                return iterations

            self.grid = new_grid

    def display_grid(self):
        right = max(int(i.real) for i in self.grid)
        bottom = min(int(i.imag) for i in self.grid)

        for y in range(0, bottom - 1, -1):
            chars = []
            for x in range(right + 1):
                state = self.grid.get(x + (1j * y))
                chars.append("#" if state else "." if state is None else "L")

            print("".join(chars))


def part_one(puzzle_input: str) -> int:
    grid = Grid(puzzle_input)
    grid.run_until_loop()
    return sum(grid.grid.values())


def part_two(puzzle_input: str) -> int:
    grid = Grid(puzzle_input, True)
    grid.run_until_loop()
    return sum(grid.grid.values())


assert part_one(TEST_INPUT) == 37
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 26
print(part_two(REAL_INPUT))
