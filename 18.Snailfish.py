import datetime
from binarytree import Node
exec_part = 1 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test18.txt') as f:
    INPUT_TEST = f.read()

with open('input/input18.txt') as f:
    INPUT = f.read()   

# Recursively parse a nested list to a binarytree object. Return root node of the tree.
# Resulting binary tree: leave nodes = regular numbers; parent nodes = pairs. Values of parent nodes = -1  
def list_2_tree(list_data):
    left_data, right_data = list_data
    n = Node(-1)
    n.left = Node(left_data) if isinstance(left_data, int) else list_2_tree(left_data)
    n.right = Node(right_data) if isinstance(right_data, int)  else list_2_tree(right_data)
    return n

def parse_input(input):
    return [list_2_tree(eval(r)) for r in input.split('\n')]

# Recursively find first explodable node (node at depth = 4 and is not a leaf node) in a binary tree
# Depth First Search/ preorder traversal (root => left sub-tree => right sub-tree)
def first_explodable(node, depth=0):
    if depth == 4 and node.value == -1:
        return node
    if node.value != -1: # leaf node
        return None
    left_explodable = first_explodable(node.left, depth+1)
    right_explodable = first_explodable(node.right, depth+1)
    if left_explodable is not None: return left_explodable
    else: return right_explodable

# Do a single reduce step
def reduce(root):
    all_nodes = root.preorder # Return a list of nodes by preorder traversal (root => left sub-tree => right sub-tree)
    leaves = [n for n in all_nodes if n.value != -1]
    for n in all_nodes:
        # Explode
        explode_node = first_explodable(root)
        if explode_node is not None:
            explode_left, explode_right = explode_node.left, explode_node.right
            # Add left value to first regular number to the left of the exploding pair, if any
            explode_left_index = leaves.index(explode_left)
            if(explode_left_index > 0):
                leaves[explode_left_index - 1].value += explode_left.value
             # Add right value to first regular number to the right of the exploding pair, if any
            explode_right_index = leaves.index(explode_right)
            if(explode_right_index < len(leaves)-1):
                leaves[explode_right_index + 1].value += explode_right.value
            # Reset exploding pair to regular number 0
            explode_node.value = 0
            del explode_node[1]
            del explode_node[2]
            return True
        # Split
        if n in leaves and n.value > 9:
            left_num, right_num = sorted([n.value // 2, n.value - n.value//2])
            n.value = -1
            n.left = Node(left_num)
            n.right = Node(right_num)
            return True
    return False

# Recursively calculate magnitude value
def magnitude(node):
    if node.value != -1: return node.value
    else: return 3 * magnitude(node.left) + 2 * magnitude(node.right)

# Add 2 snailfish number n1, n2 represented as binary trees. Return root of the resulting binary tree
def add(n1, n2):
    # Create binary tree representing unreduced addition of 2 numbers
    sum_root = Node(-1)
    sum_root.left = n1
    sum_root.right = n2
    # Reduce the sum until no further possible
    more_reduced = True
    while more_reduced:
        more_reduced = reduce(sum_root)
    return sum_root

def part1(input):
    sum_root = input[0]
    for n in input[1:]:
        sum_root = add(sum_root, n)
    return magnitude(sum_root)

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

