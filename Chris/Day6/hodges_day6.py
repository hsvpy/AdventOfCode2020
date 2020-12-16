import re
from typing import List


def parse_input_part_1(filename: str) -> str:
    with open(filename, 'r') as f:
        the_lines = re.sub('\n(?!\n)', '', f.read(), 0, re.M)        
        return the_lines.split('\n')

def parse_input_part_2(filename: str) -> List[List[str]]:
    with open(filename, 'r') as f:
        the_lines = f.readlines()
        questions = []
        group = 0        
        for line in the_lines:
            if(line == '\n'):              
                group += 1
            elif group == len(questions):
                questions.append([line.strip('\n')])
            else:
                questions[group].append(line.strip('\n'))
    return questions

    
groups = parse_input_part_1('input.txt')
sum_of_any_counts = sum(map(lambda x: len(set(x)), groups))
print(f"Part 1: {str(sum_of_any_counts)}")

questions = parse_input_part_2('input.txt')
sum = 0
for group in questions:
    for char in group[0]:
        if all(map(lambda x: char in x, group)):
            sum += 1
print(f"Part 2: {str(sum)}")