import datetime
import os
from typing import NamedTuple

exec_part = 1  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test04.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input04.txt')) as f:
    INPUT = f.read()

class Card(NamedTuple):
    winning_numbers: tuple[int]
    card_numbers: tuple[int]

def parse_input(input):
    cards = []
    for row in [r.split(': ')[1].replace('  ', ' ').strip() for r in input.split('\n')]:
        winning_numbers, card_numbers = row.split(' | ')
        cards.append(Card(tuple(int(n) for n in winning_numbers.split(' ')), tuple(int(n) for n in card_numbers.split(' '))))
    return cards

def part1(cards):
    points = 0
    for card in cards:
        winning_count = len(set(card.winning_numbers).intersection(set(card.card_numbers)))
        points = points + 2**(winning_count-1) if winning_count > 0 else points
    return points

def part2(cards):
    return 0


if __name__ == "__main__":
    if (exec_test_case == 0):
        inputs = [INPUT]
    else:
        inputs = INPUT_TEST.split("\n#####INPUT_SEPERATOR#####\n")

    if exec_test_case > len(inputs):
        print(f"Test case {exec_test_case} does not exist")
        quit()
    for i, input_str in enumerate(inputs):
        if (exec_test_case == 0):
            print("Running real puzzle input...")
        elif (exec_test_case == -1):
            print(f"Running test case {i+1}/{len(inputs)}...")
        else:
            if (i + 1 == exec_test_case):
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
