import datetime
import os

import libraries.simpleframe as sf
import numpy as np
from libraries.simpleframe import SimpleFrame

exec_part = 2 # which part to execute
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
    signal_strength = 0
    for c in range(1, 221):
        res = cpu.tick()
        if c in [20, 60, 100, 140, 180, 220] and res is not None:
            signal_strength += c * res[0]
    return signal_strength


class Screen(SimpleFrame):
    def _draw_sprite(self, sprite, row, lit_pixel):
        self.draw_tile((sprite[0], row), sf.RED)
        if lit_pixel:
            self.draw_tile((sprite[1], row), sf.GREEN)
        else:
            self.draw_tile((sprite[1], row), sf.RED)
        self.draw_tile((sprite[2], row), sf.RED)

    def _draw_screen(self, screen_pos):
        for r in range(screen_pos.shape[0]):
            for c in range(screen_pos.shape[1]):
                if (screen_pos[r][c] == 1):
                    self.draw_tile((c, r), sf.BLUE)

    def draw(self, cpu):
        screen_pos = np.zeros((6, 40), dtype=int)
        for r in range(screen_pos.shape[0]):
            for c in range(screen_pos.shape[1]):
                sprite_pos = cpu.tick()
                if sprite_pos is None: 
                    break
                sprite = range(sprite_pos[0] - 1, sprite_pos[0] + 2)
                lit_pixel = False
                if c in sprite:
                    screen_pos[r][c] = 1
                    lit_pixel = True
                self.reset_background()
                self._draw_sprite(sprite, r, lit_pixel)
                self._draw_screen(screen_pos)
                self.refresh()
                self.check_closed()

        self.reset_background()
        self._draw_screen(screen_pos)
        self.refresh()

        while(True):
            self.check_closed()

def part2(input):
    cpu = CPU(input)
    screen = Screen(width = 1000, height = 400, tile_size = 20, frame_rate=0.05)
    screen.set_title("Cathode screen")
    screen.draw(cpu)
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

