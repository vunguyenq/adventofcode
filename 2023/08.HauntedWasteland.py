import datetime
import os
from itertools import cycle

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test08.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input08.txt')) as f:
    INPUT = f.read()

class Node:
    node_name: str
    left_node: str
    right_node: str

def parse_input(input):
    rows = input.split('\n')
    instructions = cycle([c for c in rows[0]])
    nodes = {}
    for row in rows[2:]:
        node = Node()
        node.node_name = row.split(' = ')[0]
        node.left_node, node.right_node = row.split(' = ')[1][1:-1].split(', ')
        nodes[node.node_name] = node
    return instructions, nodes

def part1(input):
    instructions, nodes = input
    current_node = 'AAA'
    steps = 0
    while current_node != 'ZZZ':
        instruction = next(instructions)
        current_node = nodes[current_node].left_node if instruction == 'L' else nodes[current_node].right_node
        steps += 1
    return steps

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
