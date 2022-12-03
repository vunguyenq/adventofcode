import datetime
import os

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test02.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input02.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

def play(elf, me):
    if elf == me:
        return 3
    comb = elf * 10 + me
    if comb in [12, 23, 31]:
        return 6
    return 0

def part1(input):
    choices = {'A': 1, 'B': 2, 'C': 3, 'X': 1, 'Y': 2, 'Z': 3}
    scores = []
    for round in input:
        elf, me = round.split(' ')
        score = play(choices[elf], choices[me])
        scores.append(score + choices[me])
    return sum(scores)

def get_score(elf, round_result):
    if round_result == 'Y': # round needs to draw
        return 3 + elf
    wins = {1:2, 2:3, 3:1}
    loses = {1:3, 2:1, 3:2}
    if round_result == 'X': # I need to lose
        return loses[elf]
    return 6 + wins[elf]

def part2(input):
    choices = {'A': 1, 'B': 2, 'C': 3}
    scores = []
    for round in input:
        elf, round_result = round.split(' ')
        scores.append(get_score(choices[elf], round_result))
    return sum(scores)

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

