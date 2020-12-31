from typing import List


def parse_input(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        raw_cups = f.readline()
    return [int(char) for char in raw_cups]


def circular_index_gen(start_index: int, size_of_circle: int, number: int):
    index = start_index
    for idx in range(number):
        yield index % size_of_circle
        index += 1


# Hindsight: should have used a deque w/ rotate for circular buffer
def process(all_cups: List[int], current_index: int) -> (List[int], int):

    def circular_index(index: int) -> int:
        return index % size

    def split_cups(cups: List[int], current: int) -> (List[int], List[int], int):
        hole_size = 3
        drop_list = [cups[index] for index in circular_index_gen(current+1, len(cups), hole_size)]
        keep_list = [v for k,v in enumerate(cups) if v not in drop_list]
        new_current_value = cups[next(circular_index_gen(current+1+hole_size, len(cups), 1))]
        return drop_list, keep_list, new_current_value

    def get_destination(remainder: List[int], current: int) -> int:
        def dest_gen(i: int) -> int:
            next_candidate = i - 1
            for i in range(size):
                # account for 1-based numbers
                yield next_candidate % (size+1)
                next_candidate -= 1

        for candidate_dest in dest_gen(current):
            if candidate_dest in remainder:
                return candidate_dest
        raise AssertionError()

    def shift_buffer(new_list: List[int], left_shift_amount: int) -> List[int]:
        length = len(new_list)
        return [new_list[x] for x in circular_index_gen(left_shift_amount, length, length)]

    def run_process() -> (List[int], List[int], int):
        dropped_three, the_rest, new_current_value = split_cups(all_cups, current_index)
        destination = get_destination(the_rest, all_cups[current_index])
        t = circular_index(the_rest.index(destination)+1)
        new_list = the_rest[0:t] + dropped_three + the_rest[t:]
        new_current_index = circular_index(current_index+1)
        new_list = shift_buffer(new_list, circular_index(new_list.index(new_current_value) - new_current_index + size))
        return new_list, new_current_index

    size = len(all_cups)
    return run_process()


def cups_after_1(almost_done: List[int]) -> str:
    size = len(almost_done)
    return ''.join([str(almost_done[i]) for i in circular_index_gen(almost_done.index(1)+1, size, size-1)])



def run():
    cups = parse_input('input.txt')
    current = 0
    for i in range(100):
        cups, current = process(cups, current)
    print(f"Part 1: {cups_after_1(cups)}")


run()
