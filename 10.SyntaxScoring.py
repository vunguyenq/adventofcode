import datetime

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test10.txt') as f:
    INPUT_TEST = f.read()

with open('input/input10.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return input.split('\n')

open_chars = '([{<'
close_chars = ')]}>'

def find_corrupted_rows(input):
    corrupted_rows = []
    first_corrupted_chars = []
    for row in input:
        # Use a stack to store open brackets. When a close bracket is found, check with the last close bracket.
        open_stack = []
        for c in row:
            if c in open_chars: 
                open_stack.append(c)
            else:
                last_open_char = open_stack.pop()
                if last_open_char != open_chars[close_chars.find(c)]:
                    #print(f"Expect {close_chars[open_chars.find(last_open_char)]}, found {c}. Row: {row}")
                    first_corrupted_chars.append(c)
                    corrupted_rows.append(row)
                    break
    return corrupted_rows, first_corrupted_chars

def part1(input):
    char_scores = {')':3, ']': 57, '}': 1197, '>': 25137}
    _, first_corrupted_chars = find_corrupted_rows(input)
    return sum([char_scores[c] for c in first_corrupted_chars])

def part2(input):
    char_scores = {')':1, ']': 2, '}': 3, '>': 4}
    open_close_map = dict(zip(list(open_chars), list(close_chars)))
    corrupted_rows, _ = find_corrupted_rows(input)
    incomplete_rows = [r for r in input if r not in corrupted_rows]
    all_scores = []
    # Similar to part 1, now calculate completion string based on open characters left in the stack after scanning entire line
    for row in incomplete_rows:
        open_stack = []
        score = 0
        for c in row:
            if c in open_chars: 
                open_stack.append(c)
            else:
                open_stack.pop()
        completion_str = [open_close_map[c] for c in reversed(open_stack)]
        for c in completion_str:
            score = score * 5 + char_scores[c]
        all_scores.append(score)
    return sorted(all_scores)[len(all_scores)//2]

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

