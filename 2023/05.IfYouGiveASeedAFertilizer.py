import datetime
import os

import pandas as pd

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test05.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input05.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    parts = input.split('\n\n')
    seeds = list(map(int, parts[0].split(': ')[1].split(' ')))
    maps = []
    for m in [p.split('\n')[1:] for p in parts[1:]]:
        data = [r.split(' ') for r in m]
        headers = ['destination', 'source', 'range']
        df = pd.DataFrame(data, columns=headers).astype('int64')
        maps.append(df)
    return seeds, maps

def map_source_to_dest(df_map, source):
    for _, row in df_map.iterrows():
        if source >= row['source'] and source <= row['source'] + row['range']:
            return row['destination'] + source - row['source']
    return source

def part1(input):
    seeds, maps = input
    locations = []
    for seed in seeds:
        dest = seed
        for df_map in maps:
            dest = map_source_to_dest(df_map, dest)
        locations.append(dest)
    return min(locations)

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
