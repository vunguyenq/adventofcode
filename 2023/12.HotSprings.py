import datetime
import itertools
import os

import numpy as np

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test12.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input12.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    spring_records = []
    spring_conditions = []
    for row in input.split("\n"):
        condition, record = row.split(' ')
        spring_conditions.append(np.array([c for c in condition.replace('.', '0').replace('#', '1').replace('?', '2')], dtype=int))

        spring_records.append(tuple(map(int, record.split(','))))
    return spring_conditions, spring_records

def get_spring_record(spring_condition):
    change_points = np.diff(spring_condition, prepend=0, append=0)
    return tuple(len(segment) for segment in np.split(spring_condition, np.where(change_points != 0)[0]) if np.all(segment == 1) if len(segment) > 0)

def find_combinations(n, n_ones):
    '''Generate all possible ordered combinations of 0s and 1s with fixed number of 1s.'''
    all_combinations = itertools.product([0, 1], repeat=n)
    valid_combinations = [comb for comb in all_combinations if comb.count(1) == n_ones]
    return valid_combinations

def get_unknown_damage_count(spring_condition, spring_record):
    unknown_count = np.count_nonzero(spring_condition == 2)
    damage_count = sum(spring_record) - np.count_nonzero(spring_condition == 1)
    return unknown_count, damage_count

def count_possible_arrangements(spring_condition, spring_record):
    unknown_count, damage_count = get_unknown_damage_count(spring_condition, spring_record)
    combinations = find_combinations(unknown_count, damage_count)
    n_arrangements = 0
    for combination in combinations:
        condition = spring_condition.copy()
        condition[condition == 2] = combination
        if get_spring_record(condition) == spring_record:
            n_arrangements += 1
    return n_arrangements

def part1(input):
    spring_conditions, spring_records = input
    n_possible_arrangements = []
    rows = zip(spring_conditions, spring_records)
    n_rows = len(spring_conditions)
    for i, row in enumerate(rows):
        spring_condition, spring_record = row
        unknown_count, damage_count = get_unknown_damage_count(spring_condition, spring_record)
        print(f"{datetime.datetime.now()} \t Row {i + 1}/{n_rows}. Row length: {len(spring_condition)}. Unknowns: {unknown_count}. Known damage: {damage_count}.")
        n_possible_arrangements.append(count_possible_arrangements(spring_condition, spring_record))
    return sum(n_possible_arrangements)

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
