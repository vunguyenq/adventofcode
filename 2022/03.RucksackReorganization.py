import datetime
import os

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test03.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input03.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def get_priority(item):
    if item >= 'a' and item <= 'z': return ord(item) - ord('a') + 1
    if item >= 'A' and item <= 'Z': return ord(item) - ord('A') + 27    
    return None

def part1(input):
    priorities = []
    for r in input:
        mid_pos = len(r) // 2
        c1, c2 = list(r[:mid_pos]), list(r[mid_pos:])
        shared_item = set(c1).intersection(set(c2)).pop()
        priorities.append(get_priority(shared_item))
    return sum(priorities)

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

