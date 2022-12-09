import datetime
import os

import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test09.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input09.txt')) as f:
    INPUT = f.read()

class Rope():
    def __init__(self, head_pos) -> None:
        self.head = head_pos
        self.tail = np.copy(head_pos)

    def move_head(self, direction):
        direction_map = {
            'U': np.array([-1, 0]),
            'D': np.array([1, 0]),
            'L': np.array([0, -1]),
            'R': np.array([0, 1]),
        }
        self.head += direction_map[direction]
        self._move_tail()
    
    def _is_touching(self):
        if np.max(np.abs(self.head - self.tail)) <= 1: # Overlap or adjacent
            return True
        return False

    def _move_tail(self):
        if not(self._is_touching()):
            row_step = self.head[0] - self.tail[0]
            row_step = row_step // abs(row_step) if row_step != 0 else row_step
            col_step = self.head[1] - self.tail[1]
            col_step = col_step // abs(col_step) if col_step != 0 else col_step
            self.tail += np.array([row_step, col_step])

def parse_input(input):
    return [(p[0], int(p[1])) for p in [r.split(' ') for r in input.split('\n')]]

def part1(input):
    rope = Rope(np.array([0, 0]))
    tail_positions = []
    for direction, steps in input:
        for _ in range(steps):
            rope.move_head(direction)
            tail_positions.append(tuple(rope.tail))
    return len(set(tail_positions))

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

