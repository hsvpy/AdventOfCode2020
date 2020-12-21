from typing import Dict, Iterable, List
from collections import defaultdict
import re

import networkx

TEST_INPUT = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".split(
    "\n\n"
)

SEA_MONSTER = """                  #
#    ##    ##    ###
 #  #  #  #  #  #   """

# by counting
HASH_IN_SEA_MONSTER = 15

# or in regex form
SEA_MONSTER_REGEXES = [
    re.compile(r"..................#."),
    re.compile(r"#....##....##....###"),
    re.compile(r".#..#..#..#..#..#..."),
]

EXPECTED_PART_TWO_GRID = """.####...#####..#...###..
#####..#..#.#.####..#.#.
.#.#...#.###...#.##.O#..
#.O.##.OO#.#.OO.##.OOO##
..#O.#O#.O##O..O.#O##.##
...#.#..##.##...#..#..##
#.##.#..#.#..#..##.#.#..
.###.##.....#...###.#...
#.####.#.#....##.#..#.#.
##...#..#....#..#...####
..#.##...###..#.#####..#
....#.##.#.#####....#...
..##.##.###.....#.##..#.
#...#...###..####....##.
.#.##...#.##.#.#.###...#
#.###.#..####...##..#...
#.###...#.##...#.##O###.
.O##.#OO.###OO##..OOO##.
..O#.O..O..O.#O##O##.###
#.#..##.########..#..##.
#.#####..#.#...##..#....
#....##..#.#########..##
#...#.....#..##...###.##
#..###....##.#...##.##.#""".replace(
    "O", "#"
).splitlines()


with open("day20.txt") as infile:
    REAL_INPUT = infile.read().split("\n\n")


class Tile:
    def __init__(self, tile_number: int, tile: List[str]):
        self.tile_number = tile_number
        self.tile = self.parse_tile(tile)

    @property
    def boundaries(self) -> Dict[str, List[bool]]:
        boundaries = {
            "left": [],
            "right": [],
            "top": [],
            "bottom": [],
        }
        x_values = sorted(int(i.real) for i in self.tile)
        y_values = sorted(int(i.imag) for i in self.tile)
        min_x = x_values[0]
        max_x = x_values[-1]
        min_y = y_values[0]
        max_y = y_values[-1]
        for pos, value in self.tile.items():
            real = int(pos.real)
            imag = int(pos.imag)
            if real == min_x:
                boundaries["left"].append((pos.imag, value))
            if real == max_x:
                boundaries["right"].append((pos.imag, value))
            if imag == max_y:
                boundaries["top"].append((pos.real, value))
            if imag == min_y:
                boundaries["bottom"].append((pos.real, value))
        assert all(len(value) == 10 for value in boundaries.values()), boundaries
        return {key: list(i[1] for i in sorted(val)) for key, val in boundaries.items()}

    def make_numeric_boundaries(self) -> Dict[str, List[int]]:
        result = {
            direction: [
                int("".join(str(int(i)) for i in boundary), 2),
                int("".join(str(int(i)) for i in reversed(boundary)), 2),
            ]
            for direction, boundary in self.boundaries.items()
        }

        return result

    def parse_tile(self, tile: List[str]) -> Dict[complex, bool]:
        grid = {}
        for y, row in enumerate(tile):
            for x, char in enumerate(row):
                active = char == "#"
                grid[x - (1j * y)] = active
        return grid

    def rotate(self, left: bool = True):
        if left:
            rotation_factor = 1j
        else:
            rotation_factor = -1j
        self.tile = {
            coordinate * rotation_factor: value
            for coordinate, value in self.tile.items()
        }

    def flip_vertical(self):
        self.tile = {
            int(coordinate.real) - (1j * int(coordinate.imag)): value
            for coordinate, value in self.tile.items()
        }
        self.numeric_boundaries = self.make_numeric_boundaries()

    def __str__(self) -> str:
        return str(self.tile_number)

    def __repr__(self) -> str:
        return f"<Tile: {self.tile_number}>"

    def __eq__(self, other) -> bool:
        try:
            return self.tile_number == other.tile_number
        except AttributeError:
            return False

    def render_interior(self) -> List[str]:
        """Convert all but the outer rows/columns back into lists of strings"""
        y_values = sorted(set(int(i.imag) for i in self.tile))
        x_values = sorted(set(int(i.real) for i in self.tile))
        # these values are for excluding the boundaries
        max_x = x_values[-1]
        min_x = x_values[1]
        max_y = y_values[-1]
        min_y = y_values[1]
        result = [
            "".join(
                "#" if self.tile[x + (1j * y)] else "." for x in range(min_x, max_x)
            )
            for y in reversed(range(min_y, max_y))
        ]
        return result


def parse_tiles(puzzle_input: List[str]) -> List[Tile]:
    tiles = []
    for tile in puzzle_input:
        lines = tile.splitlines()
        tile_number = int("".join(i for i in lines[0] if i.isdigit()))
        tiles.append(Tile(tile_number, lines[1:]))
    return tiles


def potential_matches(tile: Tile, tiles: List[Tile]):
    potentials = []
    boundaries = set(tuple(i) for i in tile.boundaries.values())
    boundaries |= set(tuple(reversed(i)) for i in boundaries)
    for candidate in tiles:
        if candidate == tile:
            continue
        if set(tuple(i) for i in candidate.boundaries.values()).intersection(
            boundaries
        ):
            potentials.append(candidate)
            continue
        for _ in range(3):
            # handle rotate left, flip x, and rotate right
            candidate.rotate()
            if set(tuple(i) for i in candidate.boundaries.values()).intersection(
                boundaries
            ):
                potentials.append(candidate)
            break
        else:
            # rotate back to normal then flip Y to see if that works
            candidate.rotate()
            candidate.flip_vertical()
            if set(tuple(i) for i in candidate.boundaries.values()).intersection(
                boundaries
            ):
                potentials.append(candidate)
    return potentials


def part_one(puzzle_input: List[str]) -> int:
    tiles = parse_tiles(puzzle_input)
    corners = []
    for candidate in tiles:
        potentials = potential_matches(candidate, tiles)
        if len(potentials) == 2:
            corners.append(candidate)
    if len(corners) != 4:
        raise ValueError(
            f"found {len(corners)} corner tiles: {[i.tile_number for i in corners]}"
        )
    result = 1
    for tile in corners:
        result *= tile.tile_number
    return result


class Grid:
    def __init__(self, tiles: Iterable[Tile]):
        self.grid = self.place_tiles(tiles)
        self.verify_grid()

    def place_tiles(self, tiles: Iterable[Tile]) -> Dict[complex, Tile]:
        # square root minus 1
        max_coord = 2 if len(tiles) == 9 else 11
        neighbors: Dict[int, List[Tile]] = defaultdict(list)
        grid: Dict[complex, Tile] = {}
        tile_map: Dict[int, Tile] = {}
        for candidate in tiles:
            potentials = potential_matches(candidate, tiles)
            neighbors[candidate.tile_number] = potentials
            tile_map[candidate.tile_number] = candidate
        corners = [
            (tile_number, adjacent)
            for tile_number, adjacent in neighbors.items()
            if len(adjacent) == 2
        ]
        assert len(corners) == 4
        edges = [
            (tile_number, adjacent)
            for tile_number, adjacent in neighbors.items()
            if len(adjacent) == 3
        ]
        assert len(edges) in {4, 40}, len(edges)
        assert all(len(i) <= 4 for i in neighbors.values())
        graph = networkx.Graph()
        for tile_number, adjacent in neighbors.items():
            for adjacent_tile in adjacent:
                graph.add_edge(tile_number, adjacent_tile.tile_number)
        corner_numbers = [i[0] for i in corners]
        grid[0j] = corner_numbers[0]
        paths_to_other_corners = []
        for tile in corner_numbers[1:]:
            try:
                path = networkx.shortest_path(graph, corner_numbers[0], tile)
            except networkx.NetworkXNoPath:
                pass
            else:
                paths_to_other_corners.append(path)
        immediate_neighbors = [max_coord + 0j, -1j * max_coord]
        far_corner = None
        for path in sorted(paths_to_other_corners, key=lambda k: (0 - len(k), k[-1])):
            if len(path) != max_coord + 1:
                grid[max_coord - max_coord * 1j] = path[-1]
                far_corner = path[-1]
                continue
            # coherence check: are all our paths only traversing nodes we IDed as
            # edges?
            assert all(i in {edge[0] for edge in edges} for i in path[1:-1]), [
                path,
                edges,
            ]
            coord = immediate_neighbors.pop(0)
            if coord.real:
                step = 1 + 0j
            else:
                step = -1j
            for index, node in enumerate(path[1:]):
                grid[step * (index + 1)] = node
            far_path = networkx.shortest_path(graph, path[-1], far_corner)
            assert len(far_path) == max_coord + 1
            # need to go from either (2 + 0j) or (0 - 2j) to (2 - 2j) in the test case
            delta = (max_coord - (max_coord * 1j)) - coord
            assert delta in (max_coord, max_coord * -1j), delta
            if delta.real:
                step = 1 + 0j
            else:
                step = -1j
            for index, node in enumerate(far_path):
                if not index:
                    continue
                pos = coord + (step * index)
                if node == path[-1]:
                    assert pos == max_coord
                    assert grid[pos] == node
                    continue
                grid[pos] = node

        for pos, node in sorted(grid.items(), key=lambda k: (k[0].real, k[0].imag)):
            if int(pos.real) == 0:
                # left edge
                # so get the right side
                far_side = grid[max_coord + 1j * pos.imag]
                path = networkx.shortest_path(graph, node, far_side)
                for index, node1 in enumerate(path):
                    if not index:
                        continue
                    if node1 == far_side:
                        assert grid[max_coord + 1j * pos.imag] == node1
                        continue
                    grid[index + 1j * pos.imag] = node1
        assert len(grid) == len(tiles), (len(grid), len(tiles))
        grid = self.align_tiles(grid, neighbors, tile_map)
        return grid

    def align_tiles(
        self,
        grid: Dict[complex, int],
        neighbors: Dict[int, List[Tile]],
        tile_map: Dict[int, Tile],
    ) -> Dict[complex, Tile]:
        max_coord = 2 if len(grid) == 9 else 11
        reverse_grid = {node: pos for pos, node in grid.items()}
        adjacent_mapping = {
            # delta: [node a boundary, node b boundary],
            1 + 0j: ["right", "left"],
            -1 + 0j: ["left", "right"],
            -1j: ["bottom", "top"],
            1j: ["top", "bottom"],
        }
        tiles_set = set()
        # work from the corners first, then top left to bottom right
        coordinates = [
            0j,
            max_coord + 0j,
            max_coord - 1j * max_coord,
            -1j * max_coord,
        ]
        for y in range(0, 0 - max_coord - 1, -1):
            for x in range(max_coord + 1):
                if x + 1j * y not in coordinates:
                    coordinates.append(x + 1j * y)

        for pos in coordinates:
            node = grid[pos]
            tile = tile_map[node]
            adjacent_tiles = neighbors[node]
            for neighbor in adjacent_tiles:
                neighbor_pos = reverse_grid[neighbor.tile_number]
                delta = neighbor_pos - pos
                node_boundary, neighbor_boundary = adjacent_mapping[delta]
                if (
                    tile.boundaries[node_boundary]
                    == neighbor.boundaries[neighbor_boundary]
                ):
                    tiles_set.add(node)
                    tiles_set.add(neighbor.tile_number)
                    continue
                for inversion in range(2):
                    for rotation in range(4):
                        if node not in tiles_set:
                            for my_rotation in range(4):
                                tile.rotate()
                                if (
                                    tile.boundaries[node_boundary]
                                    == neighbor.boundaries[neighbor_boundary]
                                ):
                                    tiles_set.add(node)
                                    tiles_set.add(neighbor.tile_number)
                                    break
                                tile.flip_vertical()
                                if (
                                    tile.boundaries[node_boundary]
                                    == neighbor.boundaries[neighbor_boundary]
                                ):
                                    tiles_set.add(node)
                                    tiles_set.add(neighbor.tile_number)
                                    break
                                # flip back
                                tile.flip_vertical()

                        if (
                            tile.boundaries[node_boundary]
                            == neighbor.boundaries[neighbor_boundary]
                        ):
                            tiles_set.add(node)
                            tiles_set.add(neighbor.tile_number)
                            break
                        neighbor.flip_vertical()
                        if (
                            tile.boundaries[node_boundary]
                            == neighbor.boundaries[neighbor_boundary]
                        ):
                            tiles_set.add(node)
                            tiles_set.add(neighbor.tile_number)
                            break
                        neighbor.flip_vertical()
                        neighbor.rotate()

                    if node in tiles_set:
                        break
                    neighbor.flip_vertical()
                else:
                    raise ValueError(
                        f"No matchup found between tile {node} ({pos}) and tile"
                        f" {neighbor.tile_number} ({neighbor_pos})"
                    )

        # I think that's it
        return {pos: tile_map[node_number] for pos, node_number in grid.items()}

    def verify_grid(self):
        """Assert that all pieces are lined up cleanly"""
        x_values = sorted(int(i.real) for i in self.grid)
        y_values = sorted((int(i.imag) for i in self.grid), reverse=True)
        adjacent_mapping = {
            # delta: [node a boundary, node b boundary],
            1 + 0j: ["right", "left"],
            -1 + 0j: ["left", "right"],
            -1j: ["bottom", "top"],
            1j: ["top", "bottom"],
        }
        for y in y_values:
            for x in x_values:
                pos = x + 1j * y
                for other_pos, (my_boundary, their_boundary) in {
                    pos + delta: conditions
                    for delta, conditions in adjacent_mapping.items()
                }.items():
                    if (
                        int(other_pos.real) not in x_values
                        or int(other_pos.imag) not in y_values
                    ):
                        continue
                    assert (
                        self.grid[pos].boundaries[my_boundary]
                        == self.grid[other_pos].boundaries[their_boundary]
                    ), (
                        pos,
                        other_pos,
                        self.grid[pos].boundaries[my_boundary],
                        self.grid[other_pos].boundaries[their_boundary],
                    )

    def render_grid(self) -> List[str]:
        """Render the grid into a list of big ass strings"""
        x_values = sorted(int(i.real) for i in self.grid)
        y_values = sorted(int(i.imag) for i in self.grid)
        min_x = x_values[0]
        max_y = y_values[-1]
        max_x = x_values[-1]
        min_y = y_values[0]
        result = []
        for y in range(max_y, min_y - 1, -1):
            # all tiles are 10x10, minus the two boundary rows
            interim_rows = ["" for _ in range(8)]
            for x in range(min_x, max_x + 1):
                rendered = self.grid[x + 1j * y].render_interior()
                for index, row in enumerate(rendered):
                    interim_rows[index] = interim_rows[index] + row
            for row in interim_rows:
                result.append("".join(row))
        return result


def grid_to_string_list(grid: Dict[complex, str]) -> List[str]:
    result = []
    x_values = sorted(set(int(i.real) for i in grid))
    y_values = sorted(set(int(i.imag) for i in grid), reverse=True)
    for y in y_values:
        result += ["".join(grid[x + 1j * y] for x in x_values)]
    return result


def part_two(puzzle_input: List[str]) -> int:
    on_test = puzzle_input == TEST_INPUT
    expected_result_found = False
    tiles = parse_tiles(puzzle_input)
    grid = Grid(tiles)
    total_hashes = 0
    rendered = grid.render_grid()
    for line in rendered:
        total_hashes += sum(char == "#" for char in line)

    assert len(rendered) == len(rendered[0])
    if on_test:
        assert len(rendered) == len(EXPECTED_PART_TWO_GRID)
    candidates = [
        rendered,  # normal
    ]
    interim_rows = [[], [], [], [], [], [], [], []]
    grid = {
        x - 1j * y: char for y, row in enumerate(rendered) for x, char in enumerate(row)
    }
    rotated_90 = {pos * 1j: char for pos, char in grid.items()}
    rotated_180 = {pos * 1j: char for pos, char in rotated_90.items()}
    rotated_270 = {pos * -1j: char for pos, char in grid.items()}
    candidates += [
        grid_to_string_list(rotated_90),
        grid_to_string_list(rotated_180),
        grid_to_string_list(rotated_270),
    ]
    # now flip y for each of those
    candidates += [list(reversed(i)) for i in candidates]
    if on_test:
        assert any(i == EXPECTED_PART_TWO_GRID for i in candidates)

    counts = [0] * 8
    # now we render, count the number of sea monsters found, and rotate
    for count_index, rendered in enumerate(candidates):

        count = get_sea_monster_count(rendered)
        if count:
            return total_hashes - (count * HASH_IN_SEA_MONSTER)

    raise ValueError("Never got the right grid!")


def get_sea_monster_count(rendered_grid: List[str]) -> int:
    line_two_matches = [
        list(SEA_MONSTER_REGEXES[1].finditer(line)) for line in rendered_grid
    ]
    count = 0
    for index, matches in enumerate(line_two_matches):
        if index in {0, len(rendered_grid) - 1}:
            continue
        if not matches:
            continue
        for match in matches:
            start = match.start()
            if SEA_MONSTER_REGEXES[0].match(
                rendered_grid[index - 1][start:]
            ) and SEA_MONSTER_REGEXES[2].match(rendered_grid[index + 1][start:]):
                count += 1
    return count


assert part_one(TEST_INPUT) == 20899048083289
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 273
print(part_two(REAL_INPUT))
