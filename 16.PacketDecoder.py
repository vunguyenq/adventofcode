import datetime
import math 

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test16.txt') as f:
    INPUT_TEST = f.read()

with open('input/input16.txt') as f:
    INPUT = f.read()   

class Packet:
    def __init__(self, input_str):
        self.version = int(input_str[:3], 2)
        self.type_id = int(input_str[3:6], 2)
        self.value = None
        self.sub_packets = []
        self.remaining_bits = ''

        if self.type_id == 4: # literal value packet
            packet_data = input_str[6:]
            packet_value_str = ''
            for i in range(len(packet_data) // 5):
                packet_value_str += packet_data[i*5+1: i*5+5]
                if packet_data[i*5] == '0':
                    break
            self.value = int(packet_value_str, 2)
            self.remaining_bits = packet_data[i*5+5:]
        else: # operator packet
            if input_str[6] == '0': # length type ID = 0
                sub_pkg_bit_length = int(input_str[7:7+15], 2)
                sub_pkg_bits = input_str[7+15: 7+15+sub_pkg_bit_length]
                self.remaining_bits = input_str[7+15+sub_pkg_bit_length:]
                while(len(sub_pkg_bits) >= 11):
                    sub_packet = Packet(sub_pkg_bits)
                    self.sub_packets.append(sub_packet)
                    sub_pkg_bits = sub_packet.remaining_bits
            else: # length type ID = 1
                sub_pkg_count = int(input_str[7:7+11], 2)
                sub_pkg_bits = input_str[7+11:]
                for i in range(sub_pkg_count):
                    sub_packet = Packet(sub_pkg_bits)
                    self.sub_packets.append(sub_packet)
                    sub_pkg_bits = sub_packet.remaining_bits
                    if(len(sub_pkg_bits) == 0):
                        break
                self.remaining_bits = sub_pkg_bits
            
            # Part 2 - calculate value from sub packets
            if self.type_id == 0:
                self.value = sum([p.value for p in self.sub_packets])
            elif self.type_id == 1:
                self.value = math.prod([p.value for p in self.sub_packets])
            elif self.type_id == 2:
                self.value = min([p.value for p in self.sub_packets])
            elif self.type_id == 3:
                self.value = max([p.value for p in self.sub_packets])
            elif self.type_id == 5:
                self.value = 1 if self.sub_packets[0].value > self.sub_packets[1].value else 0
            elif self.type_id == 6:
                self.value = 1 if self.sub_packets[0].value < self.sub_packets[1].value else 0
            else: # self.type_id == 7
                self.value = 1 if self.sub_packets[0].value == self.sub_packets[1].value else 0

def parse_input(input):
    return Packet(''.join([bin(int(c,16))[2:].zfill(4) for c in input]))

def part1(input):
    flat_packet_list = [input]
    version_sum = 0
    while len(flat_packet_list) > 0:
        packet = flat_packet_list.pop()
        version_sum += packet.version
        flat_packet_list.extend(packet.sub_packets)
    return version_sum

def part2(input):
    return input.value

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

