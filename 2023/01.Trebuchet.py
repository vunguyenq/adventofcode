import datetime
import os

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test01.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input01.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return input.split('\n')

def find_first_numeric(s):
    return next((char for char in s if char.isdigit()), None)

def find_last_numeric(s):
    return next((char for char in reversed(s) if char.isdigit()), None)

def part1(input):
    return sum([int(f"{find_first_numeric(r)}{find_last_numeric(r)}") for r in input])

def replace_text_digits(input):
    digits = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    digit_input = []
    for r in input:
        for key in digits.keys():
            r = r.replace(key, f"{key}{str(digits[key])}{key}")  # 'one' -> 'one1one'
        digit_input.append(r)
    return digit_input

def part2(input):
    return sum([int(f"{find_first_numeric(r)}{find_last_numeric(r)}") for r in replace_text_digits(input)])


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
