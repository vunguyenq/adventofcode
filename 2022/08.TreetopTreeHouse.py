import datetime
import os

import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test08.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input08.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    return np.array([list(map(int, list(r))) for r in input.split('\n')])

def max_list(lst):
    if len(lst) == 0:
        return -1
    return max(lst)

def get_surrounding_trees(r, c, tree_map):
    left_trees = tree_map[r,:c]
    right_trees = tree_map[r,c+1:]
    up_trees = tree_map[:r,c]
    down_trees = tree_map[r+1:,c]
    return left_trees, right_trees, up_trees, down_trees

def check_visible(r, c, tree_map):
    tree = tree_map[r,c]
    left_trees, right_trees, up_trees, down_trees = get_surrounding_trees(r, c, tree_map)
    if (max_list(left_trees) < tree or max_list(right_trees) < tree or max_list(up_trees) < tree or max_list(down_trees) < tree):
        return True
    return False

def get_distance(val, lst):
    "Get index of first element from left of lst that are >= val"
    for i in range(len(lst)):
        if lst[i] >= val:
            return i+1
    return len(lst)

def get_scenic_score(r, c, tree_map):
    tree = tree_map[r,c]
    left_trees, right_trees, up_trees, down_trees = get_surrounding_trees(r, c, tree_map)
    left_trees = np.flip(left_trees)
    up_trees = np.flip(up_trees)
    return get_distance(tree, left_trees) * get_distance(tree, right_trees) * get_distance(tree, up_trees) * get_distance(tree, down_trees)

def part1(input):
    visible_trees = 0
    for r in range(input.shape[0]):
        for c in range(input.shape[1]):
            if check_visible(r, c, input):
                visible_trees += 1
    return visible_trees

def part2(input):
    scenic_scores = []
    for r in range(input.shape[0]):
        for c in range(input.shape[1]):
            scenic_scores.append(get_scenic_score(r, c, input))
    return max(scenic_scores)

if __name__ == "__main__":
    if(exec_test_case == 0):
        inputs = [INPUT]
    else:
        inputs = INPUT_TEST.split("\n#####INPUT_SEPERATOR#####\n")
    
    if exec_test_case > len(inputs):
        print(f"Test case {exec_test_case} does not exist")
        quit()
    for i, input_str in enumerate(inputs):
        if(exec_test_case == 0):
            print(f"Running real puzzle input...")
        elif (exec_test_case == -1):
            print(f"Running test case {i+1}/{len(inputs)}...")
        else:
            if (i+1 == exec_test_case):
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

