import datetime
import numpy as np

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test22.txt') as f:
    INPUT_TEST = f.read()

with open('input/input22.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    steps = []
    for r in input.split('\n'):
        switch, cub_pos_txt = r.replace('x=','').replace('y=','').replace('z=','').split(' ')
        switch_code = 1 if switch == 'on' else 0
        cube_pos = [list(map(int, c.split('..'))) for c in cub_pos_txt.split(',')]
        steps.append((switch_code, cube_pos))
    return steps

def part1(input):
    cubes = np.zeros([101,101,101], dtype=np.int8)
    for switch, cube_pos in input:
        x1, x2, y1, y2, z1, z2 = [i + 50 for c in cube_pos for i in c]
        if not (np.all(np.array([p in range (0, 102) for p in [x1, x2, y1, y2, z1, z2]]))):
            continue
        cubes[x1 : x2+1, y1 : y2+1, z1 : z2+1] = switch
    return np.count_nonzero(cubes == 1)


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

