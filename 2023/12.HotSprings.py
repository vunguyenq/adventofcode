import datetime
import itertools
import os
from functools import cache

import numpy as np

exec_part = 2  # which part to execute
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
        spring_conditions.append(condition)
        spring_records.append(tuple(map(int, record.split(','))))
    return spring_conditions, spring_records

# =================== Part 1 - Brute force approach ===================

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
    '''Brute forcing, try all combinations. Slight optimization by only trying combinations with the correct number of #.'''
    spring_conditions, spring_records = input
    spring_conditions = [np.array([c for c in condition.replace('.', '0').replace('#', '1').replace('?', '2')], dtype=int) for condition in spring_conditions]
    n_possible_arrangements = []
    rows = zip(spring_conditions, spring_records)
    n_rows = len(spring_conditions)
    for i, row in enumerate(rows):
        spring_condition, spring_record = row
        unknown_count, damage_count = get_unknown_damage_count(spring_condition, spring_record)
        print(f"{datetime.datetime.now()} \t Row {i + 1}/{n_rows}. Row length: {len(spring_condition)}. Unknowns: {unknown_count}. Unknown damage: {damage_count}.")
        n_possible_arrangements.append(count_possible_arrangements(spring_condition, spring_record))
    return sum(n_possible_arrangements)

# =================== Part 2 - Memoized recursive approach ===================

def print_debug(log: str, debug: bool = True):
    if debug:
        print(log)

@cache  # Memoization
def fill_unknowns(spring_condition, remaining_groups, debug=False):
    '''Attempt to fill unknowns from left to right recursively.'''

    print_debug(f"{spring_condition}, {remaining_groups}", debug=debug)

    if len(spring_condition.replace('.', '')) == 0:  # Only operational springs left
        return 1 if len(remaining_groups) == 0 else 0

    if len(remaining_groups) == 0:  # All groups have been filled while there are still tiles left
        return 0 if spring_condition.count('#') > 0 else 1

    # Not enough spaces for the remaining groups including '.' delimiters
    if len(spring_condition.replace('?', '#')) < sum(remaining_groups) + len(remaining_groups) - 1:
        return 0

    if spring_condition[0] == '.':
        return fill_unknowns(spring_condition[1:], remaining_groups, debug=debug)
    elif spring_condition[0] == '?':
        fill_1 = '.' + spring_condition[1:]
        fill_2 = '#' + spring_condition[1:]

        fill1_res = fill_unknowns(fill_1, remaining_groups, debug=debug)
        fill2_res = fill_unknowns(fill_2, remaining_groups, debug=debug)
        print_debug(f"remaining_groups: {remaining_groups}, fill1: {fill_1}, fill2: {fill_2}, fill1_res: {fill1_res}, fill2_res: {fill2_res}", debug=debug)
        return fill1_res + fill2_res
    else:  # '#'
        first_group_length = remaining_groups[0]
        first_group = spring_condition.split('.')[0]

        if len(first_group) < first_group_length:  # Spaces until the next delimiter is not enough for the first remaining group
            return 0

        if len(first_group.split('?')[0]) > first_group_length:  # Too many '#' at the beginning of the first group
            return 0

        if len(first_group) == first_group_length:  # Remaining string starts just enough '#' and '?' to fill the first group
            return 1 if len(first_group) == len(spring_condition) else fill_unknowns(spring_condition[first_group_length + 1:], remaining_groups[1:], debug=debug)

        if first_group[first_group_length] == '?':  # Remaining string starts with more '?' to fill the first group
            return fill_unknowns(spring_condition[first_group_length + 1:], remaining_groups[1:], debug=debug)
        else:  # Character right after the first group is '#' => longer than first group
            return 0


def part2(input):
    spring_conditions, spring_records = input

    # Unfolding x5
    spring_conditions = ["?".join([s] * 5) for s in spring_conditions]
    spring_records = [tuple(np.tile(arr, 5)) for arr in spring_records]

    n_possible_arrangements = []
    rows = list(zip(spring_conditions, spring_records))
    n_rows = len(spring_conditions)
    for i, row in enumerate(rows):
        spring_condition, spring_record = row
        unknown_count = spring_condition.count('?')
        damage_count = sum(spring_record) - spring_condition.count('#')
        print(f"{datetime.datetime.now()} \t Row {i + 1}/{n_rows}. Row length: {len(spring_condition)}. Unknowns: {unknown_count}. Unknown damage: {damage_count}.")
        n_possible_arrangements.append(fill_unknowns(spring_condition, spring_record))

    return sum(n_possible_arrangements)


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
