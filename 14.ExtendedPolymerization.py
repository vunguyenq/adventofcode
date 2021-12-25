import datetime
from blist import blist
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = -1 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test14.txt') as f:
    INPUT_TEST = f.read()

with open('input/input14.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    template, rules_raw = input.split('\n\n')
    rules = [row.split(' -> ') for row in rules_raw.split('\n')]
    return blist(list(template)), {tuple(r[0]): r[1] for r in rules} # Use blist instead of list for better performance on inserting to middle of list

def part1(input, nsteps = 10, progress_tracking = True):
    polymer, rules = input
    for step in range(nsteps):
        i = 0
        while (i < len(polymer)-1):
            pair = tuple(polymer[i:i+2])
            inserted_element = rules[pair] if pair in rules else None
            if inserted_element is None:
                i+=1
                continue
            polymer.insert(i+1, inserted_element)
            i+=2 # Skip newly inserted element in this step
        if(progress_tracking): print(f'Step {step} done. Polymer length: {len(polymer)}')
    frequency_counts = np.unique(np.array(polymer), return_counts=True)
    print(f"After {nsteps}, polymer length is {len(polymer)}.")
    return np.max(frequency_counts[1]) - np.min(frequency_counts[1])

def part2(input):
    return part1(input, nsteps = 40, progress_tracking = True)

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

