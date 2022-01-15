import datetime

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test21.txt') as f:
    INPUT_TEST = f.read()

with open('input/input21.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return tuple(map(int,[r.split(': ')[1] for r in input.split('\n')]))

def part1(input):
    p1_pos, p2_pos = input
    p1_score = p2_score = i = 0
    p1_turn = True
    while (p1_score < 1000 and p2_score < 1000):
        if(p1_turn):
            p1_pos = (p1_pos + 9 * i + 6 - 1) % 10 + 1
            p1_score += p1_pos
        else:
            p2_pos = (p2_pos + 9 * i + 6 - 1) % 10 + 1
            p2_score += p2_pos
        p1_turn = not(p1_turn)
        i += 1
    return i * 3 * min(p1_score, p2_score)

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

