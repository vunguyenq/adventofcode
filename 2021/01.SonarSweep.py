import datetime

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test01.txt') as f:
    INPUT_TEST = f.read()

with open('input/input01.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return list(map(int,input.split('\n')))

def part1(input):
    increase_count = 0
    for i in range(1, len(input)):
        if input[i] - input[i-1] > 0:
            increase_count += 1 
    return increase_count

def part2(input):
    increase_count = 0
    for i in range(3, len(input)):
        if sum(input[i-2:i+1]) - sum(input[i-3:i]) > 0:
            increase_count += 1 
    return increase_count

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

