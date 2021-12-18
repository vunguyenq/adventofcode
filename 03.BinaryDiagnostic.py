import datetime
import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test03.txt') as f:
    INPUT_TEST = f.read()

with open('input/input03.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    data = [tuple(map(int,tuple(row))) for row in input.split('\n')]
    return np.array(data, dtype=np.int8)

def part1(input):
    gamma_rate = epsilon_rate = '0b'
    for i in range(input.shape[1]):
        col = input[:,i]
        values, counts = np.unique(col, return_counts=True)
        count_dict = dict(zip(values, counts))
        most_common_bit = '0' if count_dict[0] > count_dict[1] else '1'
        least_common_bit = '0' if most_common_bit == '1' else '1'
        gamma_rate += most_common_bit
        epsilon_rate += least_common_bit
    return int(gamma_rate, 2) * int(epsilon_rate, 2)

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

