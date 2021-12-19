import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test05.txt') as f:
    INPUT_TEST = f.read()

with open('input/input05.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    locs = []
    for row in input.split('\n'):
        from_loc, to_loc = row.split(' -> ')
        from_loc = np.array(list(map(int,from_loc.split(','))))
        to_loc = np.array(list(map(int, to_loc.split(','))))
        locs.append((from_loc, to_loc))
    return locs

def part1(input, diagonal = False):
    max_x = max([line[0][0] for line in input] + [line[1][0] for line in input])
    max_y = max([line[0][1] for line in input] + [line[1][1] for line in input])
    ground = np.zeros((max_y + 1, max_x + 1), dtype=int)
    for line in input:
        ((x1, y1), (x2, y2)) = line
        if x1 == x2:
            min_y, max_y = min(y1, y2), max(y1, y2) + 1
            ground[min_y: max_y, x1] += 1
        elif y1 == y2:
            min_x, max_x = min(x1, x2), max(x1, x2) + 1
            ground[y1, min_x: max_x] += 1
        elif(diagonal):
            x_increment = -(x1-x2) // abs(x1-x2)
            y_increment = -(y1-y2) // abs(y1-y2)
            for i in range(abs(x1-x2)+1):
                ground[y1 + i * y_increment, x1 + i * x_increment] += 1
        else:
            continue
    return (ground > 1).sum()

def part2(input):
    return part1(input, diagonal = True)

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

