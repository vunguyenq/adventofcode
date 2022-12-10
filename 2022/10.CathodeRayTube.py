import datetime
import os

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test10.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input10.txt')) as f:
    INPUT = f.read()   

def parse_input(input):
    commands = []
    for row in [tuple(r.split(' ')) for r in input.split('\n')]:
        commands.append(row) if len(row) == 1 else commands.append((row[0], int(row[1])))
    return commands

class CPU():
    def __init__(self, instructions) -> None:
        self.x = 1
        self.instructions = instructions
        self.current_cycle = 0
        self.current_instruction = 0
        self.finished = True
    
    def tick(self):
        "Tick one single cycle. Return X value during and after cycle"
        if self.current_instruction >= len(self.instructions): # No more instruction
            return None

        self.current_cycle += 1
        instruction = self.instructions[self.current_instruction]
        if instruction[0] == 'noop':
            self.current_instruction += 1
            return (self.x, self.x)
        elif instruction[0] == 'addx':
            if self.finished: # 1st of 2 cycle of addx instruction
                self.finished = False
                return (self.x, self.x)
            else: # 2nd cycle
                self.finished = True
                current_x = self.x
                self.x += instruction[1]
                self.current_instruction += 1
                return(current_x, self.x)
        return None

def part1(input):
    cpu = CPU(input)
    signal_strength =0
    for c in range(1, 221):
        res = cpu.tick()
        if c in [20, 60, 100, 140, 180, 220] and res is not None:
            signal_strength += c * res[0]
    return signal_strength

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

