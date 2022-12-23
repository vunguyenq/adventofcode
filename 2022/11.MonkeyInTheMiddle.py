import datetime
import math
import os

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test11.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input11.txt')) as f:
    INPUT = f.read()   

class Monkey:
    def __init__(self, items, operation, test_division) -> None:
        self.items = items
        self.operation = operation
        self.test_division = test_division
        self.worry_dividen = 3
        self.worry_control = None
        self.items_inspected = 0

    def set_catching_monkeys(self, monkey_if_true, monkey_if_false):
        self.monkey_if_true = monkey_if_true
        self.monkey_if_false = monkey_if_false

    def set_worry_dividen(self, worry_dividen):
        self.worry_dividen = worry_dividen
    
    def set_worry_control(self, worry_control):
        self.worry_control = worry_control

    def inspect_next_item(self):
        if len(self.items) > 0:
            old = self.items.pop(0)
            item = (eval(self.operation)) // self.worry_dividen
            if self.worry_control is not None:
                item = item % self.worry_control
            if item % self.test_division == 0:
                self.throw_item(item, self.monkey_if_true)
            else:
                self.throw_item(item, self.monkey_if_false)
            self.items_inspected += 1
    
    def inspect_all_items(self):
        for  _ in range(len(self.items)):
            self.inspect_next_item()

    def throw_item(self, item, monkey):
        monkey.catch_item(item)

    def catch_item(self, item):
        self.items.append(item)

def parse_input(input):
    monkeys = []
    catching_monkeys = []
    # Initialize monkeys
    for i, monkey_notes in enumerate(input.split('\n\n')):
        rows = monkey_notes.split('\n')
        starting_items = list(map(int, rows[1].split(': ')[1].split(', ')))
        operation = rows[2].split('= ')[1]
        test_division = int(rows[3].split('divisible by ')[1])
        monkey_if_true = int(rows[4].split('to monkey ')[1])
        monkey_if_false = int(rows[5].split('to monkey ')[1])
        monkeys.append(Monkey(starting_items, operation, test_division))
        catching_monkeys.append((monkey_if_true, monkey_if_false))
    
    # Set monkeys to catch thrown items
    for i, monkey in enumerate(monkeys):
        monkey.monkey_if_true = monkeys[catching_monkeys[i][0]]
        monkey.monkey_if_false = monkeys[catching_monkeys[i][1]]
    return monkeys

def process_one_round(monkeys):
    for monkey in monkeys:
        monkey.inspect_all_items()


def part1(input):
    monkeys = input
    for _ in range(20):
        process_one_round(monkeys)   
    inspect_counts = sorted([m.items_inspected for m in monkeys])
    return inspect_counts[-1] * inspect_counts[-2]

# I didn't figure out how to keep worry level of items from growing to big after each inspection.
# Implemented the hint by reddit.com/user/Rangsk/ in this thread https://www.reddit.com/r/adventofcode/comments/zihouc/2022_day_11_part_2_might_need_to_borrow_a_nasa/
def part2(input):
    monkeys = input
    worry_control = math.prod([m.test_division for m in monkeys])
    for m in monkeys:
        m.set_worry_dividen(1)
        m.set_worry_control(worry_control)
    for r in range(10000):
        process_one_round(monkeys)
    inspect_counts = sorted([m.items_inspected for m in monkeys])
    return inspect_counts[-1] * inspect_counts[-2]

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

