import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test09.txt') as f:
    INPUT_TEST = f.read()

with open('input/input09.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return np.array([list(map(int,(list(row)))) for row in input.split('\n')], dtype=int)

def find_adjacents(r, c, nrow, ncol):
    adjacents = []
    if c-1 >= 0: adjacents.append((r, c-1))
    if c+1 < ncol: adjacents.append((r, c+1))
    if r-1 >= 0: adjacents.append((r-1, c))
    if r+1 < nrow: adjacents.append((r+1, c))
    return adjacents

def find_low_points(input):
    nrow, ncol = input.shape
    low_points = []
    for r in range(nrow):
        for c in range(ncol):
            height = input[r,c]
            adjacent_values = [input[x[0],x[1]] for x in find_adjacents(r, c, nrow, ncol)]
            if height < min(adjacent_values):
                low_points.append((r,c))
    return low_points

def part1(input):
    return sum(input[p[0], p[1]] + 1 for p in find_low_points(input))

def part2(input):
    nrow, ncol = input.shape
    low_points = find_low_points(input)
    all_basin_sizes = []
    # Traverse from low points, add next points to a stack
    for p in low_points:
        next_points = [p]
        basin_points = []
        while len(next_points) > 0:
            current_point = next_points.pop()
            adjacents = find_adjacents(current_point[0], current_point[1], nrow, ncol)
            next_points.extend([point for point in adjacents 
                                    if  input[point[0], point[1]] < 9 
                                    and input[point[0], point[1]] > input[current_point[0], current_point[1]]
                                    and point not in basin_points]
                                    )
            if current_point not in basin_points: basin_points.append(current_point)
        all_basin_sizes.append(len(basin_points))
    return np.prod(sorted(all_basin_sizes)[-3:])

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

