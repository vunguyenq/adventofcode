import datetime
import os

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test02.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input02.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    games = []
    for game in input.split('\n'):
        game_sets = []
        for game_set in game.split(': ')[1].split('; '):
            set_dict = {}
            for pair in game_set.split(', '):
                set_dict[pair.split(' ')[1]] = int(pair.split(' ')[0])
            game_sets.append(set_dict)
        games.append(game_sets)
    return games


def part1(input):
    impossible_games = []
    for i, game in enumerate(input):
        for game_set in game:
            reds = int(game_set['red']) if 'red' in game_set else 0
            greens = int(game_set['green']) if 'green' in game_set else 0
            blues = int(game_set['blue']) if 'blue' in game_set else 0
            if reds > 12 or greens > 13 or blues > 14:
                impossible_games.append(i + 1)
                break
    return sum([i for i in range(1, len(input) + 1) if i not in impossible_games])

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
