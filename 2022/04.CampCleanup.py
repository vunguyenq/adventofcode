import datetime
import os

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test04.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input04.txt')) as f:
    INPUT = f.read()   

# Convert string '1-2' to tuple (1,2)
def get_pair(txt):
    return tuple(map(int, txt.split('-')))

def parse_input(input):
    return [(get_pair(l), get_pair(r)) 
                for l,r in [p.split(',') for p in input.split('\n')]]

def range_contain(r1, r2):
    r1 = set(range(r1[0], r1[1]+1))
    r2 = set(range(r2[0], r2[1]+1))
    if r1.issubset(r2) or r2.issubset(r1):
        return True
    return False

def range_intersect(r1, r2):
    r1 = set(range(r1[0], r1[1]+1))
    r2 = set(range(r2[0], r2[1]+1))
    return r1.intersection(r2)

def part1(input):
    return sum([range_contain(*p) for p in input])

def part2(input):
    return 0

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

