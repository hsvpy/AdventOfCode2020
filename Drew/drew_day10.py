"""Day 10: charging stuff"""


from typing import List
from networkx import DiGraph, dfs_edges, all_simple_edge_paths
from networkx.algorithms import traversal

TEST_INPUT = [
    int(i)
    for i in """16
10
15
5
1
11
7
19
6
12
4""".split()
]


SECOND_TEST_INPUT = [
    int(i)
    for i in """28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3""".split()
]

with open("day10.txt") as infile:
    REAL_INPUT = [int(i) for i in infile]


def max_joltage(puzzle_input: List[int]):
    return max(puzzle_input) + 3


def part_one(puzzle_input: List[int]):
    outputs = sorted([0, max_joltage(puzzle_input)] + puzzle_input)
    one_volts = 0
    three_volts = 0
    for last_plug, current_plug in zip(outputs[:-1], outputs[1:]):
        if current_plug - last_plug == 1:
            one_volts += 1
        elif current_plug - last_plug == 3:
            three_volts += 1
    return one_volts * three_volts


def part_two(puzzle_input: List[int]) -> int:
    """Find all valid combinations"""
    target = max_joltage(puzzle_input)
    graph = DiGraph()
    traversal_targets = sorted(puzzle_input + [0, target])
    for index, source in enumerate(traversal_targets):
        possible_targets = [i for i in traversal_targets[index + 1 : index + 4]]
        for target in possible_targets:
            if target in range(source + 1, source + 4):
                graph.add_edge(source, target)

    result = list(all_simple_edge_paths(graph, 0, target))
    return len(result)


def part_two_alt(puzzle_input: List[int]) -> int:
    """Find all valid combinations of chargers, but use a little shortcut:

    If we have a sequence of n, n + 3, n + 6 after sorting the list, we *must* have a single
    valid path in that section. Therefore, we can break up the graph into smaller chunks at that
    middle node and multiply the number of inbound paths by the number of outbound paths.

    With the second test input, this found breaks (n+3 values in the description above) at 14, 28,
    and 42.

    With my puzzle input, this found breaks at 13, 23, 26, 35, 61, 108, 122, and 150.
    """
    target = max_joltage(puzzle_input)
    result = 1
    graph = DiGraph()
    traversal_targets = sorted(puzzle_input + [0, target])
    last_source = 0
    for index, source in enumerate(traversal_targets):
        possible_targets = [i for i in traversal_targets[index + 1 : index + 4]]
        if (
            index > 1
            and traversal_targets[index - 1] == source - 3
            and possible_targets
            and possible_targets[0] == source + 3
        ):
            # we have a single path here. Break up the graph and multiply the result by the number of paths
            result *= len(list(all_simple_edge_paths(graph, last_source, source)))
            last_source = source
            graph = DiGraph()
        for target in possible_targets:
            if target in range(source + 1, source + 4):
                graph.add_edge(source, target)

    result *= len(list(all_simple_edge_paths(graph, last_source, target)))
    return result


assert part_one(TEST_INPUT) == 35
assert part_one(SECOND_TEST_INPUT) == 220
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 8
assert part_two_alt(TEST_INPUT) == 8
assert part_two(SECOND_TEST_INPUT) == 19208
assert part_two_alt(SECOND_TEST_INPUT) == 19208
print(part_two_alt(REAL_INPUT))
