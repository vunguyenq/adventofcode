import datetime
import os
from collections import deque

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test05.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input05.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    all_boxes = [[] for i in range(10)]

    boxes_raw, moves_raw = input.split('\n\n')
    for row in boxes_raw.split('\n'):
        for i, c in enumerate(row):
            if (i-1) % 4 == 0 and c.isalpha():
                col = (i-1) // 4 + 1
                all_boxes[col].insert(0, c)
    all_boxes = [deque(col) for col in all_boxes]

    moves = [tuple(map(int, m.replace('move ', '').replace('from ', '').replace('to ', '').split(' '))) for m in moves_raw.split('\n')]
    return all_boxes, moves

def move_boxes(all_boxes, moves):
    for nbox, from_col, to_col in moves:
        for _ in range(nbox):
            box = all_boxes[from_col].pop()
            all_boxes[to_col].append(box)

def part1(input):
    all_boxes, moves = input
    move_boxes(all_boxes, moves)
    return ''.join([col.pop() for col in all_boxes if len(col) > 0])

def part2(input):
    return 0

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

