"""day 7: I'm so worried about the baggage retrieval system they've got at Heathrow"""
import networkx
from collections import defaultdict
from typing import Dict, List


TEST_INPUT = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.""".splitlines()


PART_TWO_TEST = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.""".splitlines()


with open("day07.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def parse_input(puzzle_input: List[str]) -> networkx.DiGraph:
    """Parse the puzzle input for part 1 by making a graph of what is contained by what"""
    graph = networkx.DiGraph()
    nodes = []
    for line in puzzle_input:
        source, targets = line[:-1].split(" bags contain ")
        for target in targets.split(", "):
            if target == "no other bags":
                # we've found an edge node
                continue
            # count = int(target.split()[0])
            color = " ".join(target.split()[1:-1])
            nodes.append((color, source))
    graph.add_edges_from(nodes)
    return graph


def part_one(graph: networkx.DiGraph) -> int:
    """Part 1: how many bags can eventually contain a shiny gold bag?"""
    result = list(graph.successors("shiny gold"))
    nodes_seen = set()
    target_nodes = set(result)
    for successor in result:
        if successor in nodes_seen:
            continue
        nodes_seen.add(successor)
        sub_result = list(graph.successors(successor))
        target_nodes |= set(sub_result)
        result += sub_result
    return len(target_nodes)


def part_two(puzzle_input: List[str]) -> int:
    """Part 2: how many bags does your shiny gold bag contain?"""
    dependencies = defaultdict(dict)
    for line in puzzle_input:
        source, targets = line[:-1].split(" bags contain ")
        for target in targets.split(", "):
            if target == "no other bags":
                # doesn't hold anything else. No need to store it
                continue
            count = int(target.split()[0])
            color = " ".join(target.split()[1:-1])
            dependencies[source][color] = count
    # get_bags_inside() counts the shiny gold bag, so we need to exclude it
    return get_bags_inside("shiny gold", dependencies) - 1


def get_bags_inside(color: str, dependency_dict: Dict[str, Dict[str, int]]) -> int:
    """Recursively count the bags stored wthin color, including itself"""
    count = 1
    inner_bags = dependency_dict[color]
    for bag_color, bag_count in inner_bags.items():
        count += bag_count * get_bags_inside(bag_color, dependency_dict)
    return count


assert part_one(parse_input(TEST_INPUT)) == 4
print(part_one(parse_input(REAL_INPUT)))
assert part_two(TEST_INPUT) == 32
assert part_two(PART_TWO_TEST) == 126
print(part_two(REAL_INPUT))
