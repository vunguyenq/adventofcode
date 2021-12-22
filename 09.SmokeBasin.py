import datetime
import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test09.txt') as f:
    INPUT_TEST = f.read()

with open('input/input09.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return np.array([list(map(int,(list(row)))) for row in input.split('\n')], dtype=int)

def part1(input):
    nrow, ncol = input.shape
    risk_sum = 0
    for r in range(nrow):
        for c in range(ncol):
            height = input[r,c]
            adjacents = []
            adjacents = adjacents + [(input[r, c-1])] if c-1 >= 0 else adjacents
            adjacents = adjacents + [(input[r, c+1])] if c+1 < ncol else adjacents
            adjacents = adjacents + [(input[r-1, c])] if r-1 >= 0 else adjacents
            adjacents = adjacents + [(input[r+1, c])] if r+1 < nrow else adjacents
            if height < min(adjacents):
                risk_sum += height + 1
    return risk_sum

def part2(input):
    result = 0
    return result

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

