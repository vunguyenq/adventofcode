import datetime
import os

import numpy as np

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test16.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input16.txt')) as f:
    INPUT = f.read()

ENCODE = {'.': 0, '/': 1, '\\': 2, '|': 3, '-': 4, 'up': 5, 'down': 6, 'left': 7, 'right': 8}
DECODE = {0: '.', 1: '/', 2: '\\', 3: '|', 4: '-', 5: 'up', 6: 'down', 7: 'left', 8: 'right'}

def parse_input(input):
    return np.array([[ENCODE[c] for c in r] for r in input.split('\n')])

def move_beam(beam_pos: tuple[int], direction: str, grid: np.ndarray, visited_states: set) -> None:
    # Energize the current tile
    r, c = beam_pos
    visited_states.add((r, c, ENCODE[direction]))
    # print(r, c, direction, visited_states, end='')

    # Move the beam
    if direction == 'up':
        r -= 1
    elif direction == 'down':
        r += 1
    elif direction == 'left':
        c -= 1
    elif direction == 'right':
        c += 1
    else:
        raise ValueError(f"Invalid direction: {direction}")

    # Check stopping conditions
    out_of_bounds = r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1]
    visited = (r, c, ENCODE[direction]) in visited_states
    if out_of_bounds or visited:
        return

    # Check type of tile the beam hits
    tile = DECODE[grid[r][c]]
    # print('\t', tile)
    if tile == '.':
        move_beam((r, c), direction, grid, visited_states)
    elif tile == '/':
        next_directions = {'up': 'right', 'down': 'left', 'right': 'up', 'left': 'down'}
        move_beam((r, c), next_directions[direction], grid, visited_states)
    elif tile == '\\':
        next_directions = {'up': 'left', 'down': 'right', 'left': 'up', 'right': 'down'}
        move_beam((r, c), next_directions[direction], grid, visited_states)
    elif tile == '|':
        if direction in ['up', 'down']:
            move_beam((r, c), direction, grid, visited_states)
        else:
            move_beam((r, c), 'up', grid, visited_states)
            move_beam((r, c), 'down', grid, visited_states)
    elif tile == '-':
        if direction in ['left', 'right']:
            move_beam((r, c), direction, grid, visited_states)
        else:
            move_beam((r, c), 'left', grid, visited_states)
            move_beam((r, c), 'right', grid, visited_states)
    else:
        raise ValueError(f"Invalid tile: {tile}")

def part1(input):
    grid = input
    visited_states = set()
    try:
        move_beam((0, -1), 'right', grid, visited_states)
    except RecursionError:
        print('RecursionError', len(visited_states))
    return len(set([(r, c) for r, c, _ in visited_states]))
    # return visited_states

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
