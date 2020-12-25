from typing import List

def parse_input(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    return list(map(lambda x: int(x), lines))

def is_sum_of_previous(current: int, previous: List[int]):
    for index, number in enumerate(previous):
        if current - number in previous:
            return True
    return False

def check_for_valid(the_list: List[int], preamble_len: int) -> List[bool]:
    indices = range(preamble_len, len(the_list)-1)
    return [is_sum_of_previous(the_list[x], the_list[x-preamble_len:x]) for x in indices]

def find_contiguous_addends(the_list: List[int], sum_list: int) -> List[int]:
    for end_index in range(len(the_list), 0, -1):
        target = length = 0
        while target < sum_list and length < end_index:
            target_list = the_list[end_index - length:end_index]
            target = sum(target_list)
            if target == sum_list:
                return target_list
            length += 1
    return []



preamble_len = 25
the_list = parse_input('input.txt')
invalid_index = check_for_valid(the_list, preamble_len).index(False) + preamble_len
invalid_number = the_list[invalid_index]
print(f'Part 1: {str(invalid_number)}')

contiguous_addends = sorted(find_contiguous_addends(the_list[0:invalid_index], invalid_number))
print(f'Part 2: {str(contiguous_addends[0] + contiguous_addends[-1])}')
