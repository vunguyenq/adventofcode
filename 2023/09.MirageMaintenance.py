import datetime
import os

import numpy as np

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test09.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input09.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return [np.array(list(map(int, r.split(' ')))) for r in input.split('\n')]

def find_next_root_diff(arr):
    return 0 if np.all(arr == 0) else arr[-1] + find_next_root_diff(np.diff(arr))

def part1(input):
    return sum([find_next_root_diff(arr) for arr in input])

def find_previous_root_diff(arr):
    return 0 if np.all(arr == 0) else arr[0] - find_previous_root_diff(np.diff(arr))

def part2(input):
    return sum([find_previous_root_diff(arr) for arr in input])


if __name__ == "__main__":
    if (exec_test_case == 0):
        inputs = [INPUT]
    else:
        inputs = INPUT_TEST.split("\n#####INPUT_SEPERATOR#####\n")

    if exec_test_case > len(inputs):
        print(f"Test case {exec_test_case} does not exist")
        quit()
    for i, input_str in enumerate(inputs):
        if (exec_test_case == 0):
            print("Running real puzzle input...")
        elif (exec_test_case == -1):
            print(f"Running test case {i+1}/{len(inputs)}...")
        else:
            if (i + 1 == exec_test_case):
                print(f"Running test case {i+1}/{len(inputs)}...")
            else:
                continue

        input = parse_input(input_str)
        start_time = datetime.datetime.now()
        if (exec_part == 1):
            result = part1(input)
        else:
            result = part2(input)
        end_time = datetime.datetime.now()

        print('Part {} time: {}'.format(exec_part, end_time - start_time))
        print('Part {} answer: {}\n'.format(exec_part, result))
