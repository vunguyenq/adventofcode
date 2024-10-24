import datetime
import os

import numpy as np

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test16.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input16.txt')) as f:
    INPUT = f.read()

ENCODE = {'.': 0, '/': 1, '\\': 2, '|': 3, '-': 4, 'up': 5, 'down': 6, 'left': 7, 'right': 8}
DECODE = {0: '.', 1: '/', 2: '\\', 3: '|', 4: '-', 5: 'up', 6: 'down', 7: 'left', 8: 'right'}
NEXT_DIRECTION_FORWARD_SLASH = {'up': 'right', 'down': 'left', 'right': 'up', 'left': 'down'}
NEXT_DIRECTION_BACKWARD_SLASH = {'up': 'left', 'down': 'right', 'left': 'up', 'right': 'down'}

def parse_input(input):
    return np.array([[ENCODE[c] for c in r] for r in input.split('\n')])

class Beam:
    def __init__(self, pos: tuple[int], direction: str):
        self.pos = pos
        self.direction = direction

class Platform:
    '''
    Platform class to keep track of the grid, energized status, visited states, and beams.
    Original beam and subsequent beams created by \\ - splits are tracked in stack self.beams.
    Every time a beam is split, the beam is terminated and the 2 new beams are added to the stack.
    '''
    def __init__(self, grid: np.ndarray):
        self.grid = grid
        self.visited_states = set()
        self.beams = []

    def add_beam(self, beam: Beam):
        self.beams.append(beam)

    def move_all_beams(self):
        while self.beams:
            beam = self.beams.pop()
            self.move_beam(beam)

    def move_beam(self, beam: Beam):
        split = False
        while True:
            r, c = beam.pos

            # Check stopping conditions
            out_of_bounds = r < 0 or r >= self.grid.shape[0] or c < 0 or c >= self.grid.shape[1]
            visited = (r, c, ENCODE[beam.direction]) in self.visited_states
            if out_of_bounds or visited or split:
                return

            # Track visited states
            self.visited_states.add((r, c, ENCODE[beam.direction]))

            # Check type of current tile
            tile = DECODE[self.grid[r][c]]
            if tile == '.':
                direction = beam.direction
            elif tile == '/':
                direction = NEXT_DIRECTION_FORWARD_SLASH[beam.direction]
            elif tile == '\\':
                direction = NEXT_DIRECTION_BACKWARD_SLASH[beam.direction]
            elif tile == '|':
                if beam.direction in ['up', 'down']:
                    direction = beam.direction
                else:
                    self.beams.append(Beam((r, c), 'up'))
                    self.beams.append(Beam((r, c), 'down'))
                    direction = 'split'
            elif tile == '-':
                if beam.direction in ['left', 'right']:
                    direction = beam.direction
                else:
                    self.beams.append(Beam((r, c), 'left'))
                    self.beams.append(Beam((r, c), 'right'))
                    direction = 'split'
            else:
                raise ValueError(f"Invalid tile: {tile}")

            # Move the beam
            if direction == 'up':
                r -= 1
            elif direction == 'down':
                r += 1
            elif direction == 'left':
                c -= 1
            elif direction == 'right':
                c += 1
            elif direction == 'split':
                split = True
                continue
            else:
                raise ValueError(f"Invalid direction: {beam.direction}")

            beam.pos = (r, c)
            beam.direction = direction

    def count_energized_tiles(self):
        return len(set([(r, c) for r, c, _ in self.visited_states]))


def part1(input):
    grid = input
    platform = Platform(grid)
    platform.add_beam(Beam((0, 0), 'right'))
    platform.move_all_beams()
    return platform.count_energized_tiles()

def part2(input):
    grid = input
    nrow, ncol = input.shape
    starting_positions = {'down': tuple((0, i) for i in range(ncol)),
                          'up': tuple((nrow - 1, i) for i in range(ncol)),
                          'right': tuple((i, 0) for i in range(nrow)),
                          'left': tuple((i, ncol - 1) for i in range(nrow))
                          }

    max_energized_tiles = 0
    for direction, positions in starting_positions.items():
        for pos in positions:
            platform = Platform(grid)
            platform.add_beam(Beam(pos, direction))
            platform.move_all_beams()
            max_energized_tiles = max(max_energized_tiles, platform.count_energized_tiles())
    return max_energized_tiles


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
