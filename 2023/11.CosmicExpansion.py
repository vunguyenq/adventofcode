import datetime
import os
from itertools import combinations

import numpy as np

exec_part = 2  # which part to execute
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

def expand_galaxies(universe, galaxy_locs, expand_factor):
    '''Update galaxy locations after each row/col expansion'''
    zero_rows = np.all(universe == 0, axis=1)
    zero_cols = np.all(universe == 0, axis=0)

    shifted_rows = 0
    for i in range(len(zero_rows)):
        if zero_rows[i]:
            galaxy_locs = [(loc[0] + expand_factor if loc[0] > i + shifted_rows else loc[0], loc[1]) for loc in galaxy_locs]
            shifted_rows += expand_factor

    shifted_cols = 0
    for i in range(len(zero_cols)):
        if zero_cols[i]:
            galaxy_locs = [(loc[0], loc[1] + expand_factor if loc[1] > i + shifted_cols else loc[1]) for loc in galaxy_locs]
            shifted_cols += expand_factor

    return galaxy_locs


def part2(input):
    galaxy_locs = [(a[0], a[1]) for a in np.argwhere(input == 1)]
    expanded_galaxy_locs = expand_galaxies(input, galaxy_locs, expand_factor=1000000 - 1)
    galaxy_pairs = list(combinations(expanded_galaxy_locs, 2))
    return sum([manhattan_distance(*pair) for pair in galaxy_pairs])


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
