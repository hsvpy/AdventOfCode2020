"""Day 18: order of operations"""

from operator import mul, add, sub, truediv
from typing import List

TEST_INPUTS = {
    "2 * 3 + (4 * 5)": (26, 46),
    "5 + (8 * 3 + 9 + 3 * 4 * 3)": (437, 1445),
    "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))": (12240, 669060),
    "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2": (13632, 23340),
}


OPERATIONS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": truediv,
}


with open("day18.txt") as infile:
    REAL_INPUT = [line.strip() for line in infile]


def parse_expr(expr: str) -> int:
    total = 0
    if "(" in expr:
        start = expr.index("(")
        end = expr.index(")", start)
        while "(" in expr[start + 1 : end]:
            start = expr.index("(", start + 1)

        return parse_expr(
            f"{expr[:start]} {parse_expr(expr[start + 1:end])} {expr[end + 1:]}"
        )

    ops = expr.split()
    next_op = None
    for index, op in enumerate(ops):
        if not index:
            total = int(op)
            continue
        if not index % 2:
            # even index: apply the operation
            assert next_op
            total = next_op(total, int(op))
        else:
            next_op = OPERATIONS[op]
    return total


def part_one(puzzle_input: List[str]) -> int:
    return sum(parse_expr(expr) for expr in puzzle_input)


def parse_input_part_two(expr: str) -> int:
    total = 0
    if "(" in expr:
        start = expr.index("(")
        end = expr.index(")", start)
        while "(" in expr[start + 1 : end]:
            start = expr.index("(", start + 1)

        return parse_input_part_two(
            f"{expr[:start]} {parse_input_part_two(expr[start + 1:end])} {expr[end + 1:]}"
        )

    ops = expr.split()
    try:
        next_plus = ops.index("+")
    except ValueError:
        # no +. good
        pass
    else:
        expr = " ".join(
            ops[: next_plus - 1]
            + [str(int(ops[next_plus - 1]) + int(ops[next_plus + 1]))]
            + ops[next_plus + 2 :]
        )
        return parse_input_part_two(expr)
    next_op = None
    for index, op in enumerate(ops):
        if not index:
            total = int(op)
            continue
        if not index % 2:
            # even index: apply the operation
            assert next_op
            total = next_op(total, int(op))
        else:
            next_op = OPERATIONS[op]
    return total


def part_two(puzzle_input: List[str]) -> int:
    return sum(parse_input_part_two(expr) for expr in puzzle_input)


def main():
    for expr, (p1_total, p2_total) in TEST_INPUTS.items():
        assert parse_expr(expr) == p1_total, expr
        assert parse_input_part_two(expr) == p2_total, (
            expr,
            parse_input_part_two(expr),
        )
    print(part_one(REAL_INPUT))
    print(part_two(REAL_INPUT))


if __name__ == "__main__":
    main()
