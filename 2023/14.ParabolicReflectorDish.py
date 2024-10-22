import datetime
import os

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test14.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input14.txt')) as f:
    INPUT = f.read()

class Platform:
    def __init__(self, n_rows, n_cols):
        self.size = (n_rows, n_cols)
        self.rounded_rocks = []
        self.cubes = []

    def draw(self):
        for r in range(self.size[0]):
            row = []
            for c in range(self.size[1]):
                if (r, c) in self.cubes:
                    row.append('#')
                elif any([r == rock.row and c == rock.col for rock in self.rounded_rocks]):
                    row.append('O')
                else:
                    row.append('.')
            print(''.join(row))

    def validate_position(self, row, col):
        if row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]:
            return False
        for cube in self.cubes:
            if cube[0] == row and cube[1] == col:
                return False
        for rock in self.rounded_rocks:
            if rock.row == row and rock.col == col:
                return False
        return True

    def tilt(self, direction):
        no_more_moves = False
        while not no_more_moves:
            no_more_moves = True
            for rock in self.rounded_rocks:
                new_pos = rock.soft_roll(direction)
                if self.validate_position(new_pos[0], new_pos[1]):
                    rock.roll(direction)
                    no_more_moves = False

    def get_total_load(self):
        total_load = 0
        for rock in self.rounded_rocks:
            total_load += self.size[0] - rock.row 
        return total_load

class RoundedRock:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def soft_roll(self, direction):
        if direction == 'north':
            return (self.row - 1, self.col)
        elif direction == 'south':
            return (self.row + 1, self.col)
        elif direction == 'west':
            return (self.row, self.col - 1)
        elif direction == 'east':
            return (self.row, self.col + 1)
        else:
            raise ValueError('Invalid direction')

    def roll(self, direction):
        new_pos = self.soft_roll(direction)
        self.row = new_pos[0]
        self.col = new_pos[1]

def parse_input(input):
    rows = input.split('\n')
    platform = Platform(len(rows), len(rows[0]))
    for r, row in enumerate(rows):
        for c, char in enumerate(row):
            if char == 'O':
                platform.rounded_rocks.append(RoundedRock(r, c))
            elif char == '#':
                platform.cubes.append((r, c))
            else:
                continue
    return platform

def part1(input):
    platform = input
    platform.tilt('north')
    return platform.get_total_load()

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
