import datetime

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test02.txt') as f:
    INPUT_TEST = f.read()

with open('input/input02.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def part1(input):
    x_pos = y_pos = 0
    for ins in input:
        instruction, value = ins.split()
        if (instruction == 'forward'):
            x_pos += int(value)
        elif (instruction == 'up'):
            y_pos -= int(value)
        else:
            y_pos += int(value)
    return x_pos * y_pos

def part2(input):
    x_pos = y_pos = aim = 0
    for ins in input:
        instruction, value = ins.split()
        if (instruction == 'forward'):
            x_pos += int(value)
            y_pos += int(value) * aim
        elif (instruction == 'up'):
            aim -= int(value)
        else:
            aim += int(value)
    return x_pos * y_pos

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

