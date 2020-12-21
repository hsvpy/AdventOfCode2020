from typing import Dict, List, Sequence, Tuple, Union
import re

TEST_RULES, TEST_MESSAGES = [
    i.splitlines()
    for i in """0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb""".split(
        "\n\n"
    )
]

P2_TEST_RULES, P2_TEST_MESSAGES = [
    i.splitlines()
    for i in """42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba""".split(
        "\n\n"
    )
]

with open("day19.txt") as infile:
    REAL_RULES, REAL_MESSAGES = [i.splitlines() for i in infile.read().split("\n\n")]


def rule_to_format_string(expr: str) -> str:
    rules = expr.split()
    return "".join("{rules[%s]}" % rule for rule in rules)


def parse_rules(rules: List[str]) -> Dict[str, str]:
    """Convert rules into a list of regex strings"""
    result = {}
    splits = [rule.split(":") for rule in rules]
    base_rules = {}
    for rule_number, expr in splits:
        base_rules[int(rule_number)] = expr.strip()
    for rule_number, expr in base_rules.items():
        if '"' in expr:
            assert len(expr) == 3, expr
            result[int(rule_number)] = expr[1]

    # ok, we've gotten our base rules
    # all our messages are comprised of just a and b
    assert len(result) == 2

    while len(result) != len(base_rules):
        for rule_number, expr in base_rules.items():
            if rule_number in result:
                continue
            if "|" in expr:
                format_str = (
                    "("
                    + "|".join(
                        f"{rule_to_format_string(sub_expr)}"
                        for sub_expr in expr.split("|")
                    )
                    + ")"
                )
            else:
                format_str = rule_to_format_string(expr)
            try:
                result[rule_number] = format_str.format(rules=result)
            except KeyError:
                pass

    return result


def part_one(rules: List[str], messages: List[str]) -> int:
    parsed_rules = parse_rules(rules)
    regex = re.compile("^" + parsed_rules[0] + "$")
    score = 0
    for message in messages:
        if regex.match(message):
            score += 1
    return score


def part_two(rules: List[str], messages: List[str]) -> int:
    """work through the rules and sub in as we go"""
    table = "\n".join(rules)
    rule_table = dict(re.findall("(\d+):(.+)", table))

    # Special rules for part 2
    rule_table["8"] = "42+"
    # make a wild guess and hope that we won't have more than 15 of a recursive rule
    rule_table["11"] = "|".join(f"{'42 ' * i} {'31 ' * i}" for i in range(1, 15))

    while len(rule_table) > 1:
        # Find a "completed" rule to substitute
        completed_rule_number, completed_rule = next(
            (rule_num, rule_expr)
            for rule_num, rule_expr in rule_table.items()
            if not re.search("\d", rule_expr)
        )
        rule_table = {
            rule_num: re.sub(
                rf"\b{completed_rule_number}\b", f"({completed_rule})", rule_expr
            )
            for rule_num, rule_expr in rule_table.items()
            if rule_num != completed_rule_number
        }

    # we're done
    # is this rule zero?
    assert list(rule_table) == ["0"]
    # trim quotes and whitespace
    regex_str = re.sub('[ "]', "", rule_table["0"])
    # add start/finish markers
    regex = re.compile(f"^{regex_str}$")
    return sum(bool(regex.match(line)) for line in messages)


def main():
    p1_test = part_one(TEST_RULES, TEST_MESSAGES)
    assert p1_test == 2, p1_test
    p1_result = part_one(REAL_RULES, REAL_MESSAGES)
    print(p1_result)
    print(part_two(REAL_RULES, REAL_MESSAGES))


if __name__ == "__main__":
    main()
