import os
import math

def load_array(filename):
    with open(filename, 'r') as file_handle:
        all_lines = file_handle.readlines()
        return list(map(int, all_lines))

def find_two_addends(array, sum):
    for num in array:
        if (sum - num) in array:
            return (num, sum - num)
    return None

def find_three_addends(array, sum):
    for num1 in array:
        for num2 in array:
            if num1 != num2 and (sum - num1 - num2) in array:
                return (num1, num2, sum - num1 - num2)
    return None

def convert_to_set(array,sum):
    return set(filter(lambda x: x < sum, array))
    
def main():
    array = load_array(os.path.join(os.getcwd(), 'input.txt'))
    normalized = convert_to_set(array, 2020)
    combination = find_two_addends(normalized, 2020)
    if combination:
        print(math.prod(list(combination)))
    else:
        print("No combo found")
    combination = find_three_addends(normalized, 2020)
    if combination:
        print(math.prod(list(combination)))
    else:
        print("No combo found")
    
if __name__ == "__main__":
    main()