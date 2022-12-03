import datetime

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test06.txt') as f:
    INPUT_TEST = f.read()

with open('input/input06.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return list(map(int,input.split(',')))

def part1(input, n_days = 80):
    # Create a dictionary to store count of fishes per mature days
    # Example: {0: 0, 1: 57, 2: 70, 3: 58, 4: 48, 5: 67, 6: 0, 7: 0, 8: 0}
    fish_day_map = dict(zip(list(range(0,9)), [0]*9)) 
    for f in input:
        fish_day_map[f] += 1
    # Each day, shift count of fishes to the left
    for i in range(n_days):
        fishes_day_0 = fish_day_map[0]
        for f in range(6):
            fish_day_map[f] = fish_day_map[f + 1]
        fish_day_map[6] = fish_day_map[7] + fishes_day_0 # fishes born 2 days ago + mature fishes that finish 7-day cycles
        fish_day_map[7] = fish_day_map[8]
        fish_day_map[8] = fishes_day_0 # newborn fishes
    return sum(fish_day_map.values())

def part2(input):
    return part1(input, n_days = 256)

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

