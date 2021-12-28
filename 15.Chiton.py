import datetime
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test15.txt') as f:
    INPUT_TEST = f.read()

with open('input/input15.txt') as f:
    INPUT = f.read()   

# Return a directed graph. Example of edge weight: (0,0) => (0,1): weight = value at (0,1); (0,1) => (0,0): weight = value at (0,0)
def parse_input(input):
    return np.array([list(map(int, list(row))) for row in input.split('\n')], dtype=np.int8)

def build_graph(np_data):
    nrow, ncol = np_data.shape
    G = nx.DiGraph()
    for r, row in enumerate(np_data):
        for c, col in enumerate(row):
            if c+1 < ncol: 
                G.add_edge((r,c), (r, c+1), weight = np_data[r, c+1])
                G.add_edge((r,c+1), (r, c), weight = np_data[r, c])
            if r+1 < nrow: 
                G.add_edge((r,c), (r+1, c), weight = np_data[r+1, c])
                G.add_edge((r+1,c), (r, c), weight = np_data[r, c])
    return G

def visualize(G):
    pos = nx.spring_layout(G)
    labels =  nx.get_edge_attributes(G,'weight')
    nx.draw_networkx(G,pos)
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.show()

def part1(input):
    np_data = input
    G = build_graph(input)
    target_pos = tuple(np_data.shape - np.array((1,1)))
    shortest_path = (nx.shortest_path(G,source=(0,0), target=target_pos, weight='weight', method='bellman-ford'))
    #visualize(G)
    return sum([np_data[pos[0], pos[1]] for pos in shortest_path[1:]])

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

