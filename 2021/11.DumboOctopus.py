import datetime
import numpy as np
from itertools import product 

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test11.txt') as f:
    INPUT_TEST = f.read()

with open('input/input11.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return np.array([list(map(int,(list(row)))) for row in input.split('\n')], dtype=int)

def find_adjacents(pos, size):
    nrow, ncol = size
    adjacents_rel = list(product([-1, 0, 1], repeat=2)) # Generate 8 relative adjacent cells
    adjacents_rel.remove((0,0))
    adjacents = [pos + np.array(a) for a in adjacents_rel]
    adjacents = [a for a in adjacents if a[0] in range(nrow) and a[1] in range(ncol)]
    return adjacents

# Run 1 single step
# Return energy statuses of octopuses after step and number of flashes during the step
def run_step(octopuses):
    nrow, ncol = octopuses.shape
    flash_count = 0
    # 1. Increase energy of all octopuses by 1
    octopuses += 1
    # 2. Flash & increase enery of nearby octopuses until no more flash
    flashes = np.zeros(octopuses.shape, dtype=bool) # Keep track of which octopuses flash in this step
    while(True): # Cascading flashes until no more flash
        no_more_flash = True
        for r in range(nrow):
            for c in range(ncol):
                energy = octopuses[r,c]
                if(energy <= 9 or flashes[r,c]): # Skip octopuses that don't have enough energy or already flashed
                    continue
                # else - octopus at (r,c) flashes
                no_more_flash = False
                flashes[r,c] = True
                flash_count += 1
                adjacents = find_adjacents(np.array((r,c)), octopuses.shape)
                for a in adjacents:
                    octopuses[a[0], a[1]] += 1
        if(no_more_flash):
            break
    # 3. Reset energy of flashed octopuses
    octopuses[octopuses > 9] = 0
    return octopuses, flash_count

def part1(input):
    octopuses = input
    flash_count = 0
    for step in range(100):
        octopuses, step_flash_count = run_step(octopuses)
        flash_count += step_flash_count
    return flash_count

def part2(input):
    octopuses = input
    step = 0
    while(True): 
        step += 1
        octopuses, step_flash_count = run_step(octopuses)
        if(step_flash_count == 100): # Loop until the step where all octopuses flash
            return step
    return None

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

