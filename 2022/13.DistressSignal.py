import datetime
import os

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test13.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input13.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    return [[eval(l) for l in p.split('\n')] for p in input.split('\n\n')]

def compare(left, right):
    """
        Recursively compare 2 values left and right
        Return 1 if values come in the right order, -1 if not, 0 if cannot decide.
    """
    if type(left) is int and type(right) is int:
        if left < right:
            return 1
        elif left > right:
            return -1
        else:
            return 0
    if type(left) is int and type(right) is list:
        return compare([left], right)
    if type(left) is list and type(right) is int:
        return compare(left, [right])
    # left and right are both lists
    for i in range(len(left)):
        if i == len(right): # right runs out of items first
            return -1
        compare_element = compare(left[i], right[i])
        if compare_element != 0:
            return compare_element
    if len(left) < len(right): # left runs out of items first
        return 1
    return 0

def part1(input):
    right_order_pairs =[]
    for i, pair in enumerate(input):
        if(compare(*pair) == 1):
            right_order_pairs.append(i+1)
    return sum(right_order_pairs)

def part2(input):
    print(input)
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

