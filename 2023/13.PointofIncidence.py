import datetime
import os

import numpy as np

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test13.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input13.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    patterns_text = input.replace('#', '1').replace('.', '0').split('\n\n')
    patterns = []
    for p in patterns_text:
        patterns.append(np.array([list(map(int, list(r))) for r in p.split('\n')]))
    return patterns

def find_mirror_row(arr: np.ndarray, compare_condition: str = 'all_matched'):
    '''
    Get index of first mirror row if any.
    mirror row = n if row[n] == row[n+1]; row[n-1] == row[n+2] and so on until one direction runs out of rows.
    Return 1-based index. Retun 0 if no mirror row found.
    '''
    rows = arr.shape[0]
    for r in range(rows)[:-1]:
        mirror_width = min(r + 1, rows - r - 1)
        upper_part = arr[r - mirror_width + 1:r + 1]
        lower_part = arr[r + 1: r + mirror_width + 1][::-1]  # Reverse rows in the lower part

        if compare_condition == 'all_matched':
            matched = np.array_equal(upper_part, lower_part)
        elif compare_condition == 'exact_1_diff':
            matched = np.sum(upper_part != lower_part) == 1
        else:
            raise ValueError('Invalid compare condition')

        if matched:
            return r + 1
    return 0

def find_mirror_column(arr: np.ndarray, compare_condition: str = 'all_matched') -> int:
    cols = arr.shape[1]
    for c in range(cols)[:-1]:
        mirror_width = min(c + 1, cols - c - 1)
        left_part = arr[:, c - mirror_width + 1:c + 1]
        right_part = arr[:, c + 1: c + mirror_width + 1][:, ::-1]  # Reverse columns in the right part

        if compare_condition == 'all_matched':
            matched = np.array_equal(left_part, right_part)
        elif compare_condition == 'exact_1_diff':
            matched = np.sum(left_part != right_part) == 1
        else:
            raise ValueError('Invalid compare condition')

        if matched:
            return c + 1
    return 0

def part1(input):
    mirror_rows = []
    mirror_columns = []
    for pattern in input:
        mirror_rows.append(find_mirror_row(pattern))
        mirror_columns.append(find_mirror_column(pattern))
    return sum(mirror_rows) * 100 + sum(mirror_columns)

def part2(input):
    mirror_rows = []
    mirror_columns = []
    for pattern in input:
        row = find_mirror_row(pattern, 'exact_1_diff')
        col = find_mirror_column(pattern, 'exact_1_diff')
        if (row, col) == (0, 0):
            row = find_mirror_row(pattern, 'all_matched')
            col = find_mirror_column(pattern, 'all_matched')
        mirror_rows.append(row)
        mirror_columns.append(col)
    return sum(mirror_rows) * 100 + sum(mirror_columns)


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
