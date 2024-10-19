import datetime
import os
from itertools import combinations

import numpy as np

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test11.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input11.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    input = input.replace('#', '1').replace('.', '0')
    universe = np.array([list(row) for row in input.split('\n')], dtype=int)
    return universe

def expand_universe(arr):
    zero_rows = np.all(arr == 0, axis=1)
    zero_cols = np.all(arr == 0, axis=0)

    # Insert zero rows and columns
    shifted_rows = 0
    for i in range(len(zero_rows)):
        if zero_rows[i]:
            arr = np.insert(arr, i + shifted_rows, 0, axis=0)
            shifted_rows += 1

    shifted_cols = 0
    for i in range(len(zero_cols)):
        if zero_cols[i]:
            arr = np.insert(arr, i + shifted_cols, 0, axis=1)
            shifted_cols += 1
    return arr

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def part1(input):
    universe = expand_universe(input)
    galaxy_locs = [(a[0], a[1]) for a in np.argwhere(universe == 1)]
    galaxy_pairs = list(combinations(galaxy_locs, 2))
    return sum([manhattan_distance(*pair) for pair in galaxy_pairs])

def part2(input):
    return 0


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
