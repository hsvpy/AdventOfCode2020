from typing import List, Dict, Generator
import math

def parse_input(filename: str) -> List[int]:
    return_list = [0]
    with open(filename, 'r') as f:
        lines = list(map(lambda x: int(x), f.read().splitlines()))
    return_list.extend(lines)
    return_list.extend([max(lines) + 3])
    return return_list

def calc_jump_distribution(adapters: List[int]) -> Dict[int, int]:
    deltas = [adapters[x+1]-y for x, y in enumerate(adapters) if x+1 < len(adapters)]
    return_dict = {
        1: 0,
        2: 0,
        3: 0
    }
    for difference in range(1, 4):
        return_dict[difference] = deltas.count(difference)
    return return_dict

def get_previous_neighbors(num: int) -> Generator[int, None, None]:
    for n in range(1, 4):
        yield num - n 
    return


def reverse_count_permutations(adapters: List[int]) -> int:
    adapters.reverse()
    paths = [0] * len(adapters)
    paths[0] = 1
    for index, n in enumerate(adapters):
        for dest in get_previous_neighbors(n):
            if dest in adapters:
                paths[adapters.index(dest)] += paths[index]
    return paths
        

adapter_jolts = sorted(parse_input('input.txt'))
distribution = calc_jump_distribution(adapter_jolts)
print(str(f"Part 1: {distribution[1] * distribution[3]}"))
permutations = reverse_count_permutations(adapter_jolts)
print(str(permutations[-1]))