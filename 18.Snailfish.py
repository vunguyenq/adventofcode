import datetime

exec_part = 1 # which part to execute
exec_test_case = 4 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test18.txt') as f:
    INPUT_TEST = f.read()

with open('input/input18.txt') as f:
    INPUT = f.read()   

class Pair:
    def __init__(self, left_element = None, right_element = None, depth = 0):
        self.left_element = left_element
        self.right_element = right_element
        self.depth = depth
    
    def print(self):
        left_str = str(self.left_element) if isinstance(self.left_element, int) else self.left_element.print()
        right_str = str(self.right_element) if isinstance(self.right_element, int) else self.right_element.print()
        return f"[{left_str},{right_str}]"
    
    def split(self, number, current_depth):
        child_left, child_right = sorted([number // 2, number - number//2])
        return Pair(child_left, child_right, current_depth + 1)
    
    def reduce(self):
        print(self.print())
        left_result = None
        if isinstance(self.left_element, int):
            if self.left_element >= 10:
                self.left_element = self.split(self.left_element, self.depth)
                return 'split'
        else:
            if self.depth < 4:
                left_result = self.left_element.reduce()
            else:
                return self.depth
        if not(left_result == None):
            return left_result

        if isinstance(self.right_element, int):
            if self.right_element >= 10:
                self.right_element = self.split(self.right_element, self.depth)
                return 'split'
        else:
            if self.depth < 4:
                return self.right_element.reduce()
            else:
                return self.depth

        return None



# Recursively parse a nested list to a Pair object
def list_2_pair(list_data, depth=0):
    left_data, right_data = list_data
    p = Pair(depth = depth)
    p.left_element = left_data if isinstance(left_data, int) else list_2_pair(left_data, depth+1)
    p.right_element = right_data if isinstance(right_data, int)  else list_2_pair(right_data, depth+1)
    return p

def parse_input(input):
    return [list_2_pair(eval(r)) for r in input.split('\n')]


def part1(input):
    test_input = eval('[[[[0,7],16],[15,[0,13]]],[1,1]]')
    #test_input = eval('[1,2]')
    t = list_2_pair(test_input)
    print(t.print())
    print(t.reduce())
    print(t.print())
    #for i in input:
    #    print(i.print())
    #return 0

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

