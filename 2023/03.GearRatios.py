import datetime
import os
from typing import NamedTuple

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test03.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input03.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return input.split('\n')

class Number(NamedTuple):
    number: int
    row: int
    start: int
    end: int

def get_numbers(input):
    numbers = []
    for row_num, row in enumerate(input):
        symbols = [c for c in row if not c.isalnum()]
        for s in symbols:
            row = row.replace(s, '.')
        row_elements = row.split('.')
        for i, element in enumerate(row_elements):
            if element.isdigit():
                start = sum([len(e) for e in row_elements[:i]]) + i
                end = start + len(element) - 1
                numbers.append(Number(int(element), row_num, start, end))
    return numbers

def get_adjacent_symbols(schematic, row_num, start, end):
    height, width = len(schematic), len(schematic[0])
    row_above = schematic[row_num - 1][max(start - 1, 0):min(end + 2, width)] if row_num > 0 else ''
    row_below = schematic[row_num + 1][max(start - 1, 0):min(end + 2, width)] if row_num < height - 1 else ''
    left_cell = schematic[row_num][max(start - 1, 0)] if start > 0 else ''
    right_cell = schematic[row_num][min(end + 1, width - 1)] if end < width - 1 else ''
    return ''.join(c for c in (row_above + row_below + left_cell + right_cell) if not c.isdigit() and c != '.')

def part1(input):
    numbers = get_numbers(input)
    part_numbers = []
    for number in numbers:
        if len(get_adjacent_symbols(input, number.row, number.start, number.end)) > 0:
            part_numbers.append(int(number.number))
    return sum(part_numbers)

def get_adjacent_stars(schematic, number: Number):
    adjacent_locations = []
    adjacent_locations.extend([(number.row - 1, x) for x in range(number.start - 1, number.end + 2)])  # row above
    adjacent_locations.extend([(number.row + 1, x) for x in range(number.start - 1, number.end + 2)])  # row below
    adjacent_locations.extend([(number.row, number.start - 1), (number.row, number.end + 1)])  # left and right

    adjacent_stars = []
    for loc in adjacent_locations:
        try:
            if schematic[loc[0]][loc[1]] == '*':
                adjacent_stars.append(loc)
        except IndexError:
            continue
    return adjacent_stars

def part2(input):
    numbers = get_numbers(input)
    stars = {}
    for number in numbers:
        for s in get_adjacent_stars(input, number):
            if s in stars:
                stars[s]['count'] += 1
                stars[s]['numbers'].append(number.number)
            else:
                stars[s] = {'count': 1, 'numbers': [number.number]}
    return sum([stars[s]['numbers'][0] * stars[s]['numbers'][1] for s in stars if stars[s]['count'] == 2])


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
