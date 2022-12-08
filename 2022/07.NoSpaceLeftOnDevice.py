import datetime
import os
from collections import deque

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test07.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input07.txt')) as f:
    INPUT = f.read()   

class TreeNode():
    def __init__(self, name, size=0, parent=None) -> None:
        self.name = name
        self.size = size
        self.parent = parent
        if (size==0):
            self.type = 'folder'
            self.child_nodes = []
        else:
            self.type = 'file'

    def _add_child_node(self, node):
        node.parent = self
        self.child_nodes.append(node)

    def add_file(self, name, size):
        new_file = TreeNode(name, size)
        self._add_child_node(new_file)

    def add_folder(self, name):
        new_folder = TreeNode(name)
        self._add_child_node(new_folder)
    
    def get_child_item(self, name):
        try:
            return [f for f in self.child_nodes if f.name == name][0]
        except:
            raise('File or folder does not exist')
        

    def get_size(self):
        "Calculate size of current node. If this is a folder, recursively sum size of child items"
        if self.type == 'file' or len(self.child_nodes) == 0:
            return self.size
        return sum([c.get_size() for c in self.child_nodes])

def parse_commands(input):
    commands = []
    for c in input.split('$ ')[1:]:
        cmd_lines = c.split('\n')
        cmd, cmd_result = cmd_lines[0], tuple([r for r in cmd_lines[1:] if r is not None and len(r)>0])
        commands.append((cmd, cmd_result))
    return commands

def parse_input(input):
    commands = parse_commands(input)
    root_node = TreeNode('/')
    pos = root_node
    for cmd_line, res in commands:
        cmd = cmd_line.split(' ')[0]
        if cmd == 'cd':
            dest_folder = cmd_line.split(' ')[1]
            if dest_folder == '/':
                pos = root_node
            elif dest_folder == '..':
                pos = pos.parent
            else:
                pos = pos.get_child_item(dest_folder)
        elif cmd == 'ls':
            for row in res:
                left_txt, right_txt = row.split(' ')
                if left_txt == 'dir':
                    pos.add_folder(right_txt)
                else:
                    pos.add_file(right_txt, int(left_txt))
        else:
            raise Exception(f'Unknown command: {cmd_line}')
    return root_node

def get_all_folder_size(root):
    folder_stack = deque([root])
    folder_sizes = []
    while(len(folder_stack) > 0): # DFS to traverse tree
        folder = folder_stack.pop()
        subfolders = [f for f in folder.child_nodes if f.type == 'folder']
        folder_stack.extend(subfolders)
        folder_sizes.append(folder.get_size())
    return folder_sizes

def part1(input):
    return sum([s for s in get_all_folder_size(input) if s < 100000])

def part2(input):
    root = input
    min_freeup_space = 30000000 - (70000000 - root.get_size())
    return [f for f in sorted(get_all_folder_size(root)) if f > min_freeup_space][0]

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

