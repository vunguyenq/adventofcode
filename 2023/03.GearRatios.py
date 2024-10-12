import datetime
import os

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test03.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input03.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return input.split('\n')

def get_adjacent_symbols(schematic, row_num, start, end):
    height, width = len(schematic), len(schematic[0])
    row_above = schematic[row_num - 1][max(start - 1, 0):min(end + 2, width)] if row_num > 0 else ''
    row_below = schematic[row_num + 1][max(start - 1, 0):min(end + 2, width)] if row_num < height - 1 else ''
    left_cell = schematic[row_num][max(start - 1, 0)] if start > 0 else ''
    right_cell = schematic[row_num][min(end + 1, width - 1)] if end < width - 1 else ''
    return ''.join(c for c in (row_above + row_below + left_cell + right_cell) if not c.isdigit() and c != '.')

def part1(input):
    part_numbers = []
    for row_num, row in enumerate(input):
        symbols = [c for c in row if not c.isalnum()]
        for s in symbols:
            row = row.replace(s, '.')
        row_elements = row.split('.')
        for i, element in enumerate(row_elements):
            if element.isdigit():
                start = sum([len(e) for e in row_elements[:i]]) + i
                end = start + len(element) - 1
                if len(get_adjacent_symbols(input, row_num, start, end)) > 0:
                    part_numbers.append(int(element))
    return sum(part_numbers)

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
