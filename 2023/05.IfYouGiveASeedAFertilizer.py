import datetime
import os

import pandas as pd

exec_part = 2  # which part to execute
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

def map_source_range_to_dest_ranges(df_map, source_start, source_length):
    '''
    Map source range to a list of non-overlapping destination ranges.
    Produce a list of subranges of the source range that are either (1) mapped to the a destination range or (2) no matching destination range.
    '''
    df_map['source_end'] = df_map['source'] + df_map['range']
    if source_start > df_map['source_end'].max() or source_start + source_length < df_map['source'].min():
        return [((source_start, source_start + source_length), (source_start, source_start + source_length))]

    sorted_map = df_map.sort_values(by='source')
    subranges = []
    current_start = source_start
    end = source_start + source_length
    for _, row in sorted_map.iterrows():
        # Add non-overlapping part (before the mapping range starts)
        if current_start < row['source'] and row['source'] <= end:
            source_range = dest_range = (current_start, row['source'] - 1)
            subranges.append((source_range, dest_range))

        # Add overlapping part
        if row['source'] <= end:
            overlap_start = max(row['source'], current_start)
            overlap_end = min(row['source'] + row['range'] - 1, end)
            if overlap_start <= overlap_end:
                source_range = (overlap_start, overlap_end)
                dest_range = (row['destination'] + overlap_start - row['source'], row['destination'] + overlap_end - row['source'])
                subranges.append((source_range, dest_range))

                # Update current start
                current_start = row['source'] + row['range']

    # Add the remaining part of the original range, if any
    if current_start <= end:
        source_range = dest_range = (current_start, end)
        subranges.append((source_range, dest_range))
    return subranges

def part2(input):
    seeds, maps = input
    seed_pairs = [(seeds[i], seeds[i + 1]) for i in range(0, len(seeds), 2)]
    all_location_ranges = []
    for seed in seed_pairs:
        source_ranges = [(seed[0], seed[1])]
        for df_map in maps:
            destination_ranges = []
            for source_range in source_ranges:
                subranges = map_source_range_to_dest_ranges(df_map, source_range[0], source_range[1])
                destination_ranges.extend([(r[1][0], r[1][1] - r[1][0]) for r in subranges])
            source_ranges = destination_ranges
        all_location_ranges.extend(destination_ranges)
    return f"Min location: {min([x[0] for x in all_location_ranges])}. Number of location ranges: {len(all_location_ranges)}"


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
