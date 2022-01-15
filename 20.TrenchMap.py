import datetime
from xmlrpc.client import boolean
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test20.txt') as f:
    INPUT_TEST = f.read()

with open('input/input20.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    enhance_bits, img =  input.replace('.', '0').replace('#', '1').split('\n\n')
    enhance_bits = np.array(list(map(int, list(enhance_bits))), dtype=np.int8)
    img = np.array([list(map(int, list(r))) for r in img.split('\n')], dtype=np.int8)
    return img, enhance_bits

# https://stackoverflow.com/questions/41069825/convert-binary-01-numpy-to-integer-or-binary-string
def bit_arr_2_int(bit_arr):
    return bit_arr.dot(2**np.arange(bit_arr.size)[::-1])

def enhance(img, enhance_bits, infinity_bit = 0):
    # Expand 2 rows/ cols to each edge depending on whether "infinity" is 0 or 1
    if infinity_bit == 0: 
        img_extended = np.zeros(img.shape + np.array([4,4]), dtype=np.int8)
    else: 
        img_extended = np.ones(img.shape + np.array([4,4]), dtype=np.int8)
    img_extended[2:-2,2:-2] = img
    nrow, ncol = img_extended.shape
    enhanced_img = np.copy(img_extended)
    for r in range(nrow-2):
        for c in range(ncol-2):
            i = bit_arr_2_int(img_extended[r:r+3,c:c+3].flatten())
            enhanced_img[r+1,c+1] = enhance_bits[i] 
    return enhanced_img[1:-1,1:-1] # Trim 4 edges (only zeroes/ ones) by 1 pixel each

# Execute enhancement n times on an input image
def enhance_loop(img, enhance_bits, n):
    infinity_bit = 0
    enhanced_img = np.copy(img)
    for _ in range(n):
        enhanced_img = enhance(enhanced_img, enhance_bits, infinity_bit)
        if(enhance_bits[0] == 1): # Infinity alters between 0 and 1 after each enhancement
            infinity_bit = 1 if infinity_bit == 0 else 0
    return enhanced_img

def part1(input):
    return np.sum(enhance_loop(*input, 2)) 

def part2(input):
    return np.sum(enhance_loop(*input, 50)) 

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

