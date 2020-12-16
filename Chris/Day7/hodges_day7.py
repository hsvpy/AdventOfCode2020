import re
from typing import TypedDict, List, Dict

class BagRule(TypedDict):
    class InnerBagRule(TypedDict):
        quantity: int
        color: str
    color: str
    allowed_inner: Dict[str, int]

    def allows_inner(self, color: str):
        return self.allowed_inner.count(color) > 0

def parse_input(filename: str) -> Dict[str, BagRule]:
    def parse_line(line: str) -> BagRule:        
        match = re.search(r'(^.+) bags contain', line)
        bag_color = match.group(1)
        allowed_inner = {}
        if match := re.search(r'contain no other bags', line):
            pass
        elif match := re.search(r'contain', line):
            inners = line.split("contain")[1].split(',')
            for inner in inners:
                match = re.search(r'(\d+)(.*)(?=bag)', inner)
                quantity_str = match.group(1)
                quantity = int(quantity_str)
                color = match.group(2).strip().rstrip()
                allowed_inner[color] = quantity
        return {'color': bag_color, 'allowed_inner': allowed_inner}

    with open(filename, 'r') as fd:
        lines = fd.readlines()

    rules = {}
    for line in lines:
        rule = parse_line(line)
        rules[rule['color']] = rule
    return rules

def bag_count(rules: [str, BagRule], bag_color: str) -> int:
    if not len(rules[bag_color]['allowed_inner']):
        return 1
    else:
        list_of_bag_counts = []
        for bag, count in rules[bag_color]['allowed_inner'].items():
            for _ in range(count):               
                list_of_bag_counts.append(bag_count(rules, bag)) 
        return 1 + sum(list_of_bag_counts)





rules = parse_input('input.txt')

search_bags = list(filter(lambda x: rules[x]['allowed_inner'].get('shiny gold') is not None, rules))
total_bags = []
while len(search_bags) > 0:
    total_bags.extend(search_bags)
    new_bags = []
    for bag, bag_color in enumerate(search_bags):
        new_bags.extend(list(filter(lambda x: rules[x]['allowed_inner'].get(bag_color) is not None, rules)))
    search_bags = new_bags.copy()

part1 = len(set(total_bags))
print(f"{str(part1)}")

part2 = bag_count(rules, 'shiny gold') - 1
print(f"{str(part2)}")