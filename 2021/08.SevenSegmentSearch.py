import datetime
from itertools import permutations

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test08.txt') as f:
    INPUT_TEST = f.read()

with open('input/input08.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    parsed_list = []
    for row in input.split('\n'):
        patterns, output = row.split(' | ')
        parsed_list.append(([set(n) for n in patterns.split()], [set(n) for n in output.split()]))
    return parsed_list

# Standard encoding of segments in 9 digits
segments = {0: 'abcefg', 1:'cf', 2:'acdeg', 3:'acdfg', 4:'bcdf', 5:'abdfg', 6:'abdefg', 7:'acf', 8:'abcdefg', 9:'abcdfg'}
segments = {key: set(segments[key]) for key in segments}

# Map set of segments to digit
def segments_to_digit(segment_set):
    for key in segments:
        if segments[key] == segment_set:
            return key
    return None

# Map characters in a set of segments to original digit segments
def map_char(original_segments, new_chars):
    new_char_map = dict(zip(new_chars, ['a', 'b', 'c', 'd', 'e', 'f', 'g'])) 
    return {new_char_map[c] for c in original_segments}

def part1(input):
    segment_counts_1478 = [len(segments[key]) for key in [1,4,7,8]]
    return len([i for row in input for i in row[1] if len(i) in segment_counts_1478])

def part2(input):
    output_sum = 0
    for row in input:
        for perm in list(permutations(['a', 'b', 'c', 'd', 'e', 'f', 'g'])): # Trying all permutations of segments
            correct_map = True
            for digit in row[0] + row[1]:
                original_digit = map_char(digit, perm)
                if original_digit not in segments.values(): # if a permutation results in 1 invalid digit, discard the permutation
                    correct_map = False
                    break
            if (correct_map):
                output_sum += int(''.join(list(map(str,[segments_to_digit(map_char(digit, perm)) for digit in row[1]]))))
                break  
    return output_sum

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

