import datetime
import math
import os
from functools import reduce
from itertools import cycle

exec_part = 2  # which part to execute
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

def eda_part2(input, max_visited_end_nodes=4):
    '''
    Exploratory Data Analysis. Run this function to understand the pattern in part 2.

    Sample run with max_visited_end_nodes = 4
    TTA [(1, 'KHZ', 15871), (2, 'KHZ', 31742), (3, 'KHZ', 47613), (4, 'KHZ', 63484)]
    KJA [(1, 'KRZ', 19637), (2, 'KRZ', 39274), (3, 'KRZ', 58911), (4, 'KRZ', 78548)]
    BGA [(1, 'HSZ', 12643), (2, 'HSZ', 25286), (3, 'HSZ', 37929), (4, 'HSZ', 50572)]
    AAA [(1, 'ZZZ', 14257), (2, 'ZZZ', 28514), (3, 'ZZZ', 42771), (4, 'ZZZ', 57028)]
    LTA [(1, 'DXZ', 21251), (2, 'DXZ', 42502), (3, 'DXZ', 63753), (4, 'DXZ', 85004)]
    NJA [(1, 'HRZ', 19099), (2, 'HRZ', 38198), (3, 'HRZ', 57297), (4, 'HRZ', 76396)]

    Observation: For every start node, it always takes a fixed number of steps (from start node to end node)
                 and then (from this first end node back to the same end node the 2nd time) and so on. Name this the cycle length.
    Conclusion: answer for part 2 is the LCM of all cycle lengths.
    '''
    instructions, nodes = input
    current_nodes = [n for n in nodes.keys() if n[-1] == 'A']
    end_nodes = [n for n in nodes.keys() if n[-1] == 'Z']

    for node in current_nodes:
        steps = 0
        current_node = node

        n_visited_end_nodes = 0
        visited_end_nodes = []

        while True:
            instruction = next(instructions)
            current_node = nodes[current_node].left_node if instruction == 'L' else nodes[current_node].right_node
            steps += 1
            if current_node in (end_nodes):
                n_visited_end_nodes += 1
                visited_end_nodes.append((n_visited_end_nodes, current_node, steps))
                if n_visited_end_nodes == max_visited_end_nodes:
                    break
        print(node, visited_end_nodes)

def find_cycle_length(node, input):
    instructions, nodes = input
    end_nodes = [n for n in nodes.keys() if n[-1] == 'Z']
    current_node = node
    steps = 0
    while current_node not in end_nodes:
        instruction = next(instructions)
        current_node = nodes[current_node].left_node if instruction == 'L' else nodes[current_node].right_node
        steps += 1
    return steps

def part2(input):
    # eda_part2(input, 10)
    nodes = input[1]
    start_nodes = [n for n in nodes.keys() if n[-1] == 'A']
    cycle_lengths = [find_cycle_length(node, input) for node in start_nodes]

    def lcm_list(numbers):  # Least Common Multiple of a list of numbers
        return reduce(lambda a, b: a * b // math.gcd(a, b), numbers)
    return lcm_list(cycle_lengths)


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
