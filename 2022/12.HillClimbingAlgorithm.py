import datetime
import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test12.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input12.txt')) as f:
    INPUT = f.read()   

def visualize_graph(G):
    pos = nx.spring_layout(G)
    labels =  nx.get_edge_attributes(G,'weight')
    nx.draw_networkx(G,pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()

def parse_input(input):
    """Model height map as a directed graph"""
    G = nx.DiGraph()
    height_map = np.array([[ord(c) for c in list(r)] for r in input.split('\n')])
    source_pos = tuple(np.where(height_map == ord('S')))
    dest_pos = tuple(np.where(height_map == ord('E')))
    height_map[source_pos] = ord('a')
    height_map[dest_pos] = ord('z')
    for r, row in enumerate(height_map):
        for c, chr in enumerate(row):
            adjacents = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            for a in adjacents:
                if (a[0] < 0 or a[1] < 0 or a[0] > height_map.shape[0]-1 or a[1] > height_map.shape[1]-1):
                    continue
                if height_map[r, c] + 1  >= height_map[a]:
                    G.add_edge((r,c), a)
    return G, list(zip(*source_pos))[0], list(zip(*dest_pos))[0], height_map

def part1(input):
    G, source_pos, dest_pos, _ = input
    return len(nx.shortest_path(G, source=source_pos, target=dest_pos)) - 1

def part2(input):
    G, _, dest_pos, height_map = input
    path_lengths = []
    lowest_positions = tuple(np.where(height_map == ord('a')))
    for source_pos in (list(zip(*lowest_positions))):
        try:
            path_lengths.append(len(nx.shortest_path(G, source=source_pos, target=dest_pos)) - 1)
        except nx.NetworkXNoPath:
            continue
    return min(path_lengths)

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

