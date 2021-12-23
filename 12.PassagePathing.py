import datetime
import networkx as nx

exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test12.txt') as f:
    INPUT_TEST = f.read()

with open('input/input12.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    G = nx.Graph()
    for row in input.split('\n'):
        G.add_edge(*tuple(row.split('-')))
    for n in G.nodes:
        G.nodes[n]['big_cave'] = n.isupper()
    return G

# Recursively find all paths from a given node to 'end'. 
def scan_all_paths(start_node, current_path, G):
    path_count = 0
    if start_node == 'end':
        #print(current_path)
        return path_count + 1
    # Jump to new caves or backtrack to big caves. No backtracking to small caves.
    next_nodes = [n for n in G.neighbors(start_node) if n not in [cave for cave in current_path if G.nodes[cave]['big_cave'] == False]]
    for n in next_nodes:
        next_path = current_path.copy()
        next_path.append(n)
        path_count += scan_all_paths(n, next_path, G)
    return path_count

def part1(input):
    G = input
    node_stack = ['start']
    #while(len(node_stack) > 0):
        #n = 
    return scan_all_paths('start', ['start'], G)

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

