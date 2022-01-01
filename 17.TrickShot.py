import datetime
import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test17.txt') as f:
    INPUT_TEST = f.read()

with open('input/input17.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return [tuple(map(int, cor.split('..'))) for cor in input.replace('target area:','').replace(' x=','').replace(' y=','').split(',')]   

def step(pos, vel):
    pos += vel
    if vel[0] > 0:
        vel[0] -= 1 
    elif vel[0] < 0:
        vel[0] += 1
    vel[1] -= 1
    return pos, vel

def part1(input):
    target_x, target_y = input
    max_height = 0
    # Naive approach - bruteforcing: try all initial velocities from (1,1) to (max_x, abs(min_y)). 
    # Simulate steps, pick highest y of attemps that hits target area at least once and return max(highest y)
    # Simplified solution of scanning y coordinate only does NOT work if target x range is too narrow - https://www.reddit.com/r/adventofcode/comments/rid0g3/2021_day_17_part_1_an_input_that_might_break_your/
    for x_vel in range(1, target_x[1]):
        for y_vel in range(1, abs(target_y[0])):
            pos = np.array((0,0))
            vel = np.array((x_vel, y_vel))
            max_height_attemp = 0
            hit_target = False
            while (pos[0] <= target_x[1] + 1 and pos[1] >= target_y[1] + 1):
                pos, vel = step(pos, vel)
                max_height_attemp = max(max_height_attemp, pos[1])
                if (pos[0] in range(target_x[0], target_x[1] + 1) and pos[1] in range(target_y[0], target_y[1] + 1)):
                    hit_target = True
            if(hit_target):
                max_height = max(max_height, max_height_attemp)
    return max_height

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

