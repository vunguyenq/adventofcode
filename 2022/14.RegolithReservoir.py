import datetime
import os

import libraries.simpleframe as sf
import numpy as np
from libraries.simpleframe import SimpleFrame

exec_part = 2 # which part to execute
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
    
    def __init__(self, starting_pos = np.array([0, 500]), screen = None) -> None:
        self.pos = starting_pos
        self.screen = screen

    def _move_one_step(self, direction, sand_map):
        """
            Move sand one step on direction vector.
            Returns new position of sand if movable, None if unmovable, 'fall' if sand falls off boundaries.
        """
        if self.screen is not None:
            self.screen.draw(sand_map, self.pos)

        new_pos = self.pos + direction
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

class Screen(SimpleFrame):
    _SHIFT_COL = -300
    def draw(self, sand_map, sand_pos):
        self.reset_background()
        self.draw_tile((sand_pos[1] + self._SHIFT_COL, sand_pos[0]), sf.RED)
        for r in range(sand_map.shape[0]):
            for c in range(sand_map.shape[1]):
                if sand_map[r, c] == 1:
                    self.draw_tile((c + self._SHIFT_COL, r), sf.BLUE)
                elif sand_map[r,c] == 2:
                    self.draw_tile((c + self._SHIFT_COL, r), sf.RED)
        self.refresh()
        self.check_closed()

def part1(input):
    sand_map = input
    screen = Screen(width = 1500, height = 800, tile_size = 4, frame_rate=0.01)
    screen.set_title("Day 14: Regolith Reservoir part 1")
    while(True):
        s = Sand(screen=screen) # Initialize Sand with a Screen object to visualize
        # s = Sand()
        rest_pos = s.fall(sand_map)
        if rest_pos is None:
            break
        sand_map[tuple(rest_pos)] = 2
    return np.count_nonzero(sand_map == 2)

def part2(input):
    sand_map = input
        
    # Expand map to ADD_COLS cols each size + 2 rows in the bottom
    ADD_COLS = 200
    additional_cols = np.zeros((sand_map.shape[0], ADD_COLS), dtype=np.dtype('u1'))
    empty_row = np.zeros((1, sand_map.shape[1] + ADD_COLS*2), dtype=np.dtype('u1'))
    floor_row = np.ones((1, sand_map.shape[1] + ADD_COLS*2), dtype=np.dtype('u1'))
    sand_map = np.concatenate([additional_cols, np.copy(sand_map), additional_cols], axis=1)
    sand_map = np.concatenate([sand_map, empty_row], axis=0)
    sand_map = np.concatenate([sand_map, floor_row], axis=0)

    # screen = Screen(width = 1500, height = 800, tile_size = 3, frame_rate=0.01)
    # screen.set_title("Day 14: Regolith Reservoir part 2")
    sand_pos = np.array([0, 500+ADD_COLS])
    i = 0
    while(True):
        s = Sand(starting_pos=sand_pos)
        rest_pos = s.fall(sand_map)
        if tuple(rest_pos) == tuple(sand_pos):
            break
        sand_map[tuple(rest_pos)] = 2

        # # Visualize
        # screen.draw(sand_map, sand_pos)

        # Progress tracker
        i += 1
        if (i%1000) == 0:
            print(f'Sand {i}th falling, rests at position {tuple(rest_pos)}')
    return np.count_nonzero(sand_map == 2) + 1

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

