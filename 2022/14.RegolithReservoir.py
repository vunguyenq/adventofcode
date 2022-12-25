import datetime
import os

import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test14.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input14.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    rocks = set([])
    for row in input.split('\n'):
        points = [tuple(map(int, p.split(','))) for p in row.split(' -> ')]
        for i in range(1, len(points)):
            [(from_col, from_row), (to_col, to_row)] = points[i-1:i+1]
            step_col = 1 if from_col < to_col else -1
            col_range = tuple(range(from_col, to_col+step_col, step_col))
            step_row = 1 if from_row < to_row else -1
            row_range = tuple(range(from_row, to_row+step_row, step_row))
            rocks.update([(r,c) for r in row_range for c in col_range])
    max_rocks_row = max([r[0] for r in rocks])
    max_rocks_col = max([r[1] for r in rocks])
    rock_map = np.zeros((max_rocks_row + 1, max_rocks_col + 1), dtype=np.dtype('u1'))
    for r in rocks:
        rock_map[r] = 1 # air = 0, rock = 1, sand = 2
    return rock_map

class Sand:
    _DOWN = np.array([1, 0])
    _DOWNLEFT = np.array([1, -1])
    _DOWNRIGHT = np.array([1, 1])
    
    def __init__(self) -> None:
        self.pos = np.array([0, 500])

    def _move_one_step(self, direction, sand_map):
        """
            Move sand one step on direction vector.
            Returns new position of sand if movable, None if unmovable, 'fall' if sand falls off boundaries.
        """
        new_pos = self.pos + direction
        # print(self.pos, new_pos)
        if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[0] >= sand_map.shape[0] or new_pos[1] >= sand_map.shape[1]:
            return 'fall'
        if sand_map[tuple(new_pos)] > 0: # a rock or another sand already at new_pos
            return None
        return new_pos

    def fall(self, sand_map):
        """
            Simulate falling sand.
            Returns rest position if sand rests. Otherwise return None
        """
        fall = False
        while True:
            rest = True
            for direction in [self._DOWN, self._DOWNLEFT, self._DOWNRIGHT]:
                new_pos = self._move_one_step(direction, sand_map)
                if new_pos == 'fall':
                    fall = True
                    break
                elif new_pos is not None:
                    rest = False
                    self.pos = new_pos
                    break    
            if fall:
                return None
            if rest:
                return self.pos


def part1(input):
    sand_map = input
    i = 0
    while(True):
        s = Sand()
        rest_pos = s.fall(sand_map)
        if rest_pos is None:
            break
        sand_map[tuple(rest_pos)] = 2
    return np.count_nonzero(sand_map == 2)

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

