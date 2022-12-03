import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test04.txt') as f:
    INPUT_TEST = f.read()

with open('input/input04.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    input_parts = input.split('\n\n')
    draw_numbers = list(map(int,input_parts[0].split(',')))
    boards = []
    for board in input_parts[1:]:
        boards.append(np.array([list(map(int,row.strip().split())) for row in board.split('\n')]))
    return draw_numbers, boards

# Find first winning board or last winning board depending on mode
def find_win_boards(draw_numbers, boards, mode = 'first'):
    board_masks = [np.zeros((5,5), dtype=bool) for _ in boards]
    winning_boards = [] # store indices of winning boards and winning numbers 
    for number in draw_numbers:
        for i, board in enumerate(boards):
            if(i in [p[0] for p in winning_boards]): # Skip winning boards
                continue
            (row, col) = np.where(board == number) # find indices of number board
            if len(row) == 0: # number not in board
                continue
            board_masks[i][row[0], col[0]] = True
            # Check if board wins by calculating row-wise and column-wise AND of board mask
            for j in range(5):
                row_and = np.all(board_masks[i][j,:])
                col_and = np.all(board_masks[i][:,j])
                if row_and or col_and:
                    unmarked_board = np.ma.masked_array(board, board_masks[i])
                    unmarked_sum = np.sum(unmarked_board)
                    if(mode == 'first'):
                        return unmarked_sum * number
                    elif(mode == 'last'):
                        winning_boards.append((i, number))
                        break
    last_board_win, last_number = winning_boards[-1]
    unmarked_board = np.ma.masked_array(boards[last_board_win], board_masks[last_board_win])
    unmarked_sum = np.sum(unmarked_board)
    return unmarked_sum * last_number

def part1(input):
    draw_numbers, boards = input
    return find_win_boards(draw_numbers, boards, mode = 'first')

def part2(input):
    draw_numbers, boards = input
    return find_win_boards(draw_numbers, boards, mode = 'last')

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

