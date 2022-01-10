import datetime
import numpy as np
import math
from itertools import product

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test19.txt') as f:
    INPUT_TEST = f.read()

with open('input/input19.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    return [np.array([list(map(int,row.split(','))) for row in scanner_data.split('\n')[1:]], dtype=int) for scanner_data in input.split('\n\n')]

# Generate 24 rotation matrices
# https://en.wikipedia.org/wiki/Rotation_matrix - General rotation matrix = Rx.Ry.Rz
# Rotate each axis x,y,z by (0,90,180,270) degrees => 4*4*4 = 64 combinations; Deduplicate => 24 unique rotations
def rotation_matrices():
    rot_angles_rad = [math.radians(90*i) for i in range(4)]
    rot_matrix_data = []
    for x in rot_angles_rad:
        rx = np.array([[1, 0, 0],[0, math.cos(x), -math.sin(x)],[0, math.sin(x), math.cos(x)]], dtype=np.int8)
        for y in rot_angles_rad:
            ry = np.array([[math.cos(y), 0, math.sin(y)],[0, 1, 0],[-math.sin(y), 0, math.cos(y)]], dtype=np.int8)
            for z in rot_angles_rad:
                rz = np.array([[math.cos(z), -math.sin(z), 0],[math.sin(z), math.cos(z), 0],[0, 0, 1]], dtype=np.int8)
                rot_matrix = rx.dot(ry).dot(rz) # Rx.Ry.Rz
                rot_matrix_data.append(tuple(map(tuple, rot_matrix))) # Convert array to tuple of tuple to deduplicate
    return [np.array(r, dtype=np.int8) for r in set(rot_matrix_data)]

def part1(input):
    rot_matrices = rotation_matrices()
    all_beacons = np.copy(input[0])
    identified_scanners = [0]
    # Trying to rotate beacons detected by each scanner relative to scanner 0
    while (len(identified_scanners) < len(input)):
        unidentified_scanners = [n for n in range(len(input)) if n not in identified_scanners]
        for i,j in (list(product(identified_scanners, unidentified_scanners))):
            root_beacons = input[i]
            compare_beacons = input[j]
            successful_match = False
            # Trying to rotate each of 24 orientations
            for r in rot_matrices:
                rotated_beacons = np.copy(compare_beacons).dot(r)
                # Assume 2 scanners are at the same root (0,0) and agrees in all directions, 
                # compute vector from every beacons detected by scanner 1 to every beacons detected by scanner 2
                # If any vector repeats >= 12 times, it's the position of scanner 2 relative to scanner 1
                beacon_vectors = np.array([r1-r2 for r1 in root_beacons for r2 in rotated_beacons])
                unique_vectors, counts = np.unique(beacon_vectors, axis=0, return_counts=True)
                compare_scanner_pos = None
                if np.max(counts) >= 12:
                    print(f"Identified scanner {j} ({len(identified_scanners)+1}/{len(input)} scanners)")
                    compare_scanner_pos = unique_vectors[np.argmax(counts)] # Positon of scanner relative to scanner 0
                    rotated_beacons_scanner0 = rotated_beacons + compare_scanner_pos # Compute positions of beacons relative to scanner 0
                    input[j] = rotated_beacons_scanner0
                    identified_scanners.append(j)
                    all_beacons = np.vstack((all_beacons, rotated_beacons_scanner0)) # Track all beacons having identified positions relative to scanner 0, including duplicates
                    successful_match = True
                    break
            if successful_match: break
    # Deduplicate list of all beacons 
    beacons, _ = np.unique(all_beacons, axis=0, return_counts=True)
    return len(beacons)

def part2(input):
    result = 0
    return result

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

