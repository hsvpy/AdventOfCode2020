from typing import List

def parse_input(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        lines = list(map(lambda x: int(x), f.readlines()))
    return lines

keys = parse_input("test.txt")
print(f"{str(keys)}")