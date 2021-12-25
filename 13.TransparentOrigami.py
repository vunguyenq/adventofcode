import datetime
import numpy as np
from matplotlib import pyplot as plt

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test13.txt') as f:
    INPUT_TEST = f.read()

with open('input/input13.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    dots_raw, folds_raw = input.split('\n\n')
    dots = [list(map(int, r.split(','))) for r in dots_raw.split('\n')]
    nrow = max([d[1] for d in dots]) + 1
    ncol = max([d[0] for d in dots]) + 1
    paper = np.zeros((nrow, ncol), dtype=np.int8)
    for dot in dots:
        paper[dot[1], dot[0]] = 1
    folds = [r.replace('fold along ','').split('=') for r in folds_raw.split('\n')]
    folds = [(f[0], int(f[1])) for f in folds]
    return paper, folds

# Print np array of 1, 0 in textual format with 1 = #, 0 = .
def paper_text(paper):
    return ('\n'.join(''.join(str(x) for x in y) for y in paper).replace('0','.').replace('1','#'))

# Do a single fold
def fold(paper, fold):
    fold_ax, fold_at = fold
    if fold_ax == 'y':
        folded_part = np.flipud(paper[fold_at+1:,:]) # Flip folded part up
        remaining_part = paper[0:fold_at:,:]
        longer_part = remaining_part if remaining_part.shape[0] >= folded_part.shape[0] else folded_part
        shorter_part = remaining_part if remaining_part.shape[0] < folded_part.shape[0] else folded_part
        shorter_part_padded = np.vstack([np.zeros([longer_part.shape[0] - shorter_part.shape[0], longer_part.shape[1]], dtype=np.int8), shorter_part])
        paper = longer_part + shorter_part_padded # Combine dots of 2 parts together after fold by adding 2 matrix
        paper[paper > 0] = 1 # Eliminate overlapped dots
    else:
        folded_part = np.fliplr(paper[:,fold_at+1:]) # Flip folded part up
        remaining_part = paper[:,0:fold_at:]
        longer_part = remaining_part if remaining_part.shape[1] >= folded_part.shape[1] else folded_part
        shorter_part = remaining_part if remaining_part.shape[1] < folded_part.shape[1] else folded_part
        shorter_part_padded = np.hstack([np.zeros([longer_part.shape[0], longer_part.shape[1] - shorter_part.shape[1]], dtype=np.int8), shorter_part])
        paper = longer_part + shorter_part_padded # Combine dots of 2 parts together after fold by adding 2 matrix
        paper[paper > 0] = 1 # Eliminate overlapped dots
    return paper

def part1(input):
    paper, folds = input
    paper = fold(paper, folds[0])
    return len(paper[paper == 1])

def part2(input):
    paper, folds = input
    for f in folds:
        paper = fold(paper, f)
    # Plotting 1-0 array as an pixel image 
    plt.imshow(paper, interpolation='nearest')
    plt.show()
    return '\n' + paper_text(paper)

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

