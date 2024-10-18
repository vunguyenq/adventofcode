import datetime
import os

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test10.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input10.txt')) as f:
    INPUT = f.read()

def encode_ascii_pipe(input):
    '''Encode pipe map using ascii pipe characters. Just for better visibility. And fun!'''
    return (input
            .replace('|', '║')
            .replace('-', '═')
            .replace('L', '╚')
            .replace('J', '╝')
            .replace('7', '╗')
            .replace('F', '╔')
            )

class Pipe():
    def __init__(self, pipe_loc, pipe_char, map_size):
        row, col = pipe_loc
        max_row, max_col = map_size
        self.pipe_char = pipe_char
        self.loc = pipe_loc
        if pipe_char == '║':
            self.adjacents = [(row - 1, col), (row + 1, col)]
        elif pipe_char == '═':
            self.adjacents = [(row, col - 1), (row, col + 1)]
        elif pipe_char == '╚':
            self.adjacents = [(row, col + 1), (row - 1, col)]
        elif pipe_char == '╝':
            self.adjacents = [(row, col - 1), (row - 1, col)]
        elif pipe_char == '╗':
            self.adjacents = [(row, col - 1), (row + 1, col)]
        elif pipe_char == '╔':
            self.adjacents = [(row, col + 1), (row + 1, col)]
        else:
            self.adjacents = []

        for adj in self.adjacents:
            if adj[0] < 0 or adj[0] >= max_row or adj[1] < 0 or adj[1] >= max_col:
                self.adjacents.remove(adj)

    def enter_pipe(self, from_loc):
        for adj in self.adjacents:
            if adj != from_loc:
                return adj

def parse_input(input):
    input = encode_ascii_pipe(input)
    input = input.split('\n')
    map_size = (len(input), len(input[0]))
    pipe_map = []
    animal_loc = (0, 0)
    for r, row in enumerate(input):
        pipe_map.append([Pipe((r, c), char, map_size) for c, char in enumerate(row)])
        animal_col = row.find('S')
        animal_loc = (r, animal_col) if animal_col != -1 else animal_loc
    fill_starting_pipe(pipe_map, animal_loc)        
    return pipe_map, animal_loc

def find_starting_adjacents(pipe_map, animal_loc):
    r, c = animal_loc
    adjacents = []
    for loc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
        if loc[0] >= 0 and loc[0] < len(pipe_map) and loc[1] >= 0 and loc[1] < len(pipe_map[0]) and animal_loc in pipe_map[loc[0]][loc[1]].adjacents:
            adjacents.append(loc)
    return adjacents

def fill_starting_pipe(pipe_map, animal_loc):
    starting_ajacents = find_starting_adjacents(pipe_map, animal_loc)
    map_size = (len(pipe_map), len(pipe_map[0]))
    for c in '║═╚╝╔╗':
        pipe = Pipe(animal_loc, c, map_size)
        if set(pipe.adjacents) == set(starting_ajacents):
            pipe_map[animal_loc[0]][animal_loc[1]] = pipe
            return

def travel_pipe_loop(start_loc, from_pipe, pipe_map):
    '''Travel the pipe loop starting from start_loc and record the distances to each pipe'''
    loc = start_loc
    pipe = pipe_map[loc[0]][loc[1]]
    from_loc = from_pipe
    distances = {}
    steps = 0
    while True:
        next_loc = pipe.enter_pipe(from_loc)
        if next_loc == start_loc:
            return distances
        steps += 1
        distances[next_loc] = steps
        from_loc = loc
        loc = next_loc
        pipe = pipe_map[loc[0]][loc[1]]

def part1(input):
    pipe_map, animal_loc = input
    start_pipe = pipe_map[animal_loc[0]][animal_loc[1]]

    # Travel the pipe loop starting from animal_loc from both directions
    d1, d2 = [travel_pipe_loop(animal_loc, from_loc, pipe_map) for from_loc in start_pipe.adjacents]
    return max([min(d1[k], d2[k]) for k in d1.keys()])

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
