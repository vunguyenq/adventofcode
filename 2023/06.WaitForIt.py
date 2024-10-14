import datetime
import functools
import math
import os
import re

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test06.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input06.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return input.split('\n')

def count_winning_cases(time, dist):
    '''
    Time t=x+y. We need all integer x, y such that P = xy > Distance D.
    => x(t-x) > D => We need to solve quadratic inequality f = x^2 - tx + D < 0
    '''
    delta = time ** 2 - 4 * dist
    if delta <= 0:
        winning_cases = 0  # No possible winning cases
    else:  # Compute 2 real roots x1, x2. f(x) is negative between x1 and x2.
        x1 = (time + math.sqrt(delta)) / 2
        x2 = (time - math.sqrt(delta)) / 2
        x1_int = math.ceil(x1) - 1
        x2_int = math.floor(x2) + 1
        winning_cases = x1_int - x2_int + 1
    return winning_cases


def part1(input):
    time_values, dist_values = [list(map(int, re.findall(r'\d+', row))) for row in input]
    data = list(zip(time_values, dist_values))
    all_winning_cases = []
    for time, dist in data:
        all_winning_cases.append(count_winning_cases(time, dist))
    return functools.reduce(lambda x, y: x * y, all_winning_cases)

def part2(input):
    time, dist = [int(re.findall(r'\d+', row.replace(' ', ''))[0]) for row in input]
    return count_winning_cases(time, dist)


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
