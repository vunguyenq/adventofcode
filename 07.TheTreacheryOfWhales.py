import datetime
import numpy as np

exec_part = 2# which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test07.txt') as f:
    INPUT_TEST = f.read()

with open('input/input07.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return list(map(int,input.split(',')))

# Median is the point which minimizes the sum of distances for one-dimensional data: https://en.wikipedia.org/wiki/Geometric_median
def part1(input):
    positions = np.array(input)
    return int(np.sum(abs(positions - np.median(positions))))

def part2(input):
    positions = np.array(input)
    min_pos, max_pos = np.min(positions), np.max(positions)
    min_fuel = None
    for p in range(min_pos, max_pos + 1):
        distance_func = lambda n: (abs(n-p))*(abs(n-p)+1)/2 # https://en.wikipedia.org/wiki/1_%2B_2_%2B_3_%2B_4_%2B_%E2%8B%AF
        distance = np.sum(distance_func(positions))
        if(min_fuel is None):
            min_fuel = distance
        else:
            min_fuel = min(min_fuel, distance)
    return int(min_fuel)

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

