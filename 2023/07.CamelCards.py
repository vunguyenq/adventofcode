import datetime
import os
from collections import Counter

exec_part = 2  # which part to execute
exec_test_case = 0  # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test07.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input07.txt')) as f:
    INPUT = f.read()

def parse_input(input):
    return [(r.split(' ')[0], int(r.split(' ')[1])) for r in input.split('\n')]

def encode_cards(hand: str, part: int) -> str:
    '''Encode char cards to leverage direct string comparison'''
    j_encode = 'W' if part == 1 else '1'
    text_cards = {'A': 'Z', 'K': 'Y', 'Q': 'X', 'J': j_encode, 'T': 'V'}
    return ''.join([text_cards.get(c, c) for c in hand])

def hand_type(hand: str) -> str:
    # Count the occurrences of each card in the hand
    counts = Counter(hand)
    freq = sorted(counts.values(), reverse=True)  # Sort by frequency of cards

    if freq == [5]:
        return 7  # Five of a kind
    elif freq == [4, 1]:
        return 6  # Four of a kind
    elif freq == [3, 2]:
        return 5  # Full house
    elif freq == [3, 1, 1]:
        return 4  # Three of a kind
    elif freq == [2, 2, 1]:
        return 3  # Two pair
    elif freq == [2, 1, 1, 1]:
        return 2  # One pair
    else:
        return 1  # High card

def part1(input):
    sorted_hands = sorted([(encode_cards(hand, part=1), hand_type(hand), bet) for hand, bet in input], key=lambda x: (x[1], x[0]))
    return sum([(i + 1) * h[2] for i, h in enumerate(sorted_hands)])

def impersonate_joker(hand: str) -> str:
    '''Replace the Joker with all possible cards in the hand and return the best hand'''
    if 'J' not in hand:
        return hand
    other_cards = [c for c in hand if c != 'J']
    best_hand = hand
    for c in other_cards:
        impersonated_hand = hand.replace('J', c)
        if hand_type(impersonated_hand) > hand_type(best_hand):
            best_hand = impersonated_hand
    return best_hand

def part2(input):
    sorted_hands = sorted([(encode_cards(hand, part=2), hand_type(impersonate_joker(hand)), bet, hand) for hand, bet in input], key=lambda x: (x[1], x[0]))
    return sum([(i + 1) * h[2] for i, h in enumerate(sorted_hands)])


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
