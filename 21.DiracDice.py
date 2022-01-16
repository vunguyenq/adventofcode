import datetime
from itertools import product
from collections import Counter

exec_part = 2 # which part to execute
exec_test_case = -1 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

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

# Unique values of 3 dice rolls + frequency {6: 7, 5: 6, 7: 6, 4: 3, 8: 3, 3: 1, 9: 1}
DICE_VALUES = Counter([sum(c) for c in list(product([1,2,3], repeat = 3))])
STATE_CACHE = {}

def recursive_count(p1_pos, p1_score, p2_pos, p2_score, turn):
    # Stop recursion when a player wins
    if p1_score >= 21:
        return [1, 0]
    if p2_score >= 21:
        return [0, 1]

    # Return if a state was seen before
    state_key = (p1_pos, p1_score, p2_pos, p2_score, turn)
    if state_key in STATE_CACHE:
        return STATE_CACHE[state_key]

    # Current player roll dices
    universe_count = [0, 0]
    if turn == 1:
        for dice_val in DICE_VALUES:
            new_pos = (p1_pos + dice_val - 1) %10 + 1
            new_score = p1_score + new_pos 
            #print(p1_pos, p1_score, new_pos, new_score, dice_val, DICE_VALUES[dice_val])
            universe_count[0] += DICE_VALUES[dice_val] * recursive_count(new_pos, new_score, p2_pos, p2_score, 2)[0]
    else:
        for dice_val in DICE_VALUES:
            new_pos = (p2_pos + dice_val - 1) %10 + 1
            new_score = p2_score + new_pos 
            universe_count[1] += DICE_VALUES[dice_val] * recursive_count(p1_pos, p1_score, new_pos, new_score, 1)[1]
    
    STATE_CACHE[state_key] = universe_count
    return universe_count
    # 7 unique dice combination * freq of each unique
    # Cache 
    # https://www.reddit.com/r/adventofcode/comments/rm7ygy/2021_day_21_part2_could_someone_explain_the/
    


def part2(input):
    p1_pos, p2_pos = input
    a = recursive_count(p1_pos, 0, p2_pos, 0, 1)
    print(a)
    state_keys = list(STATE_CACHE.keys())
    print(len(state_keys))
    for k in state_keys[-100:]:
        print(k, STATE_CACHE[k])
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

