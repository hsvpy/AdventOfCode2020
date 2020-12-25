from collections import defaultdict
from typing import Any, Dict, Iterable, List


TEST_INPUT = """class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12"""

with open("day16.txt") as infile:
    REAL_INPUT = infile.read()


def parse_input(puzzle_input: str) -> Dict[str, Any]:
    result = {
        "rules": {},
        "your ticket": [],
        "nearby tickets": [],
    }
    mode = "rules"
    for line in puzzle_input.splitlines():
        line = line.strip()
        if mode == "rules":
            if line:
                rule, ranges = line.split(": ")
                ranges = ranges.split(" or ")
                rules = []
                for range_str in ranges:
                    lower, upper = range_str.split("-")
                    rules.append(range(int(lower), int(upper) + 1))
                result["rules"][rule] = rules
            else:
                mode = "your ticket"
                continue
        elif mode == "your ticket":
            if line == "your ticket:":
                continue
            if line:
                result["your ticket"] = [int(i) for i in line.split(",")]
            else:
                mode = "nearby tickets"
                continue
        elif mode == "nearby tickets":
            if line == "nearby tickets:":
                continue
            if line:
                result["nearby tickets"].append([int(i) for i in line.split(",")])
            else:
                return result
        else:
            raise ValueError("state machine broke")
    return result


def get_invalid_value(ticket: List[int], rules: Dict[str, List[Iterable]]) -> int:
    """Is a ticket valid?"""
    valid_ranges = sum(rules.values(), [])
    invalid_values = 0
    for value in ticket:
        if all(value not in r for r in valid_ranges):
            invalid_values += value
    return invalid_values


def part_one(puzzle_input: str) -> int:
    puzzle = parse_input(puzzle_input)
    rules = puzzle["rules"]
    other_tickets = puzzle["nearby tickets"]
    return sum(get_invalid_value(ticket, rules) for ticket in other_tickets)


def part_two(puzzle_input: str) -> int:
    puzzle = parse_input(puzzle_input)
    rules = puzzle["rules"]
    other_tickets = puzzle["nearby tickets"]
    valid_tickets = [
        ticket for ticket in other_tickets if not get_invalid_value(ticket, rules)
    ]
    values_by_field = []
    # think of this as a very ugly means of transposing a table
    for index in range(len(valid_tickets[0])):
        values_by_field.append(list(ticket[index] for ticket in valid_tickets))
    field_map = defaultdict(lambda: list())
    for field_index, field_values in enumerate(values_by_field):
        for field_name, field_rules in rules.items():
            if all(number_in_ranges(value, field_rules) for value in field_values):
                field_map[field_name].append(field_index)
    definite_fields = {}
    for field_name, field_index_candidates in field_map.items():
        if len(field_index_candidates) == 1:
            definite_fields[field_name] = field_index_candidates[0]
    result = 1
    while field_map:
        # NOTE this runs indefinitely on mine. Let's just keep going until we get our 6
        # departure fields isolated

        # what we're doing is looping through each field to see if we have isolated the candidate
        # field indexes down to one value
        for field_name, field_index_candidates in list(field_map.items()):
            if field_name in definite_fields:
                # we've already matched it. Kill it.
                del field_map[field_name]
                continue
            for value in definite_fields.values():
                # remove that value from the candidate list
                try:
                    field_index_candidates.remove(value)
                except ValueError:
                    pass
            if len(field_index_candidates) == 1:
                # yay we've isolated one candidate
                definite_fields[field_name] = field_index_candidates[0]
        # by some miracle, have we gotten our 6?
        departure_values = list(
            val for key, val in definite_fields.items() if key.startswith("departure")
        )
        if len(departure_values) == 6:
            for i in departure_values:
                # get the values from my ticket
                result *= puzzle["your ticket"][i]
            return result

    return result


def number_in_ranges(number: int, ranges: List[Iterable]) -> bool:
    return any(number in r for r in ranges)


assert part_one(TEST_INPUT) == 71
print(part_one(REAL_INPUT))
assert part_two(TEST_INPUT) == 1
print(part_two(REAL_INPUT))
