import datetime
import os

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test15.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input15.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return input.split(',')

def compute_hash(txt):
    current_value = 0
    for c in txt:
        current_value = (current_value + ord(c)) * 17 % 256
    return current_value

class Box:
    def __init__(self, box_id: int):
        self.box_id = box_id
        self.lenses = {}

    def add_or_replace_lens(self, lens_label: str, lens_focal_length: int):
        self.lenses[lens_label] = lens_focal_length

    def remove_lens(self, lens_label: str):
        _ = self.lenses.pop(lens_label, None)

    def compute_lenses_power(self):
        return sum([(self.box_id + 1) * (i + 1) * f for i, f in enumerate(self.lenses.values())])

def part1(input):
    return sum([compute_hash(s) for s in input])

def part2(input):
    boxes = [Box(i) for i in range(256)]
    for seq in input:
        if '-' in seq:
            lens_label = seq[:-1]
            boxes[compute_hash(lens_label)].remove_lens(lens_label)
        elif '=' in seq:
            lens_label, lens_focal_length = seq.split('=')
            boxes[compute_hash(lens_label)].add_or_replace_lens(lens_label, int(lens_focal_length))
        else:
            continue
    return sum([box.compute_lenses_power() for box in boxes])


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
