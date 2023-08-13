import datetime
import os
import re
from itertools import product

from shapely.geometry import MultiPolygon, Polygon

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'input/input_test15.txt')) as f:
    INPUT_TEST = f.read()

with open(os.path.join(dirname, 'input/input15.txt')) as f:
    INPUT = f.read()   


def manhattan_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x2 - x1) + abs(y2 - y1)

class Sensor():
    def __init__(self, pos, closest_beacon_pos):
        self.pos = pos
        self.beacon_pos = closest_beacon_pos
        self.dist = manhattan_distance(pos, closest_beacon_pos)
        x, y = pos
        self.cover_area = ((x-self.dist, y), (x, y-self.dist), (x+self.dist, y), (x, y+self.dist))
    
    def covers(self, pos):
        '''Check if a position (x,y) is in coverage area of sensor'''
        if manhattan_distance(self.pos, pos) <= self.dist:
            return True
        return False
    
    def find_no_beacon_range_in_row(self, row_no):
        '''Return range of positions that can't possibly contain a beacon in a row'''
        x_range = self.dist - abs(self.pos[1] - row_no)
        if x_range < 0:
            return None
        min_x, max_x = self.pos[0] - x_range, self.pos[0] + x_range
        if self.beacon_pos[1] == row_no: # Row contains beacon
            min_x = min_x + 1 if self.beacon_pos[0] == min_x else min_x
            max_x = max_x - 1 if self.beacon_pos[0] == max_x else max_x
        return (min_x, max_x)

def parse_input(input):
    rows = input.split('\n')
    pattern = r'x=(-?\d+), y=(-?\d+)'
    sensors = []
    for r in rows:
        sensor, beacon = re.findall(pattern, r)
        sensor = tuple(map(int, sensor))
        beacon = tuple(map(int, beacon))
        sensors.append(Sensor(sensor, beacon))
    return sensors


def part1(input):
    ROW = 2000000
    unique_points = []
    for sensor in input:
        row_range = sensor.find_no_beacon_range_in_row(ROW)
        if row_range is not None:
            unique_points.extend(range(row_range[0], row_range[1] + 1))
    return len(set(unique_points))

def part2(input):
    space_size = 4000000
    sensors = input
    # Start with entire seach space as a square.
    # In each iteration, clip cover area of each sensor away from the search space
    search_space = Polygon([(0, 0), (0, space_size), (space_size, space_size), (space_size, 0)])
    for sensor in sensors:
        area = Polygon(sensor.cover_area)
        search_space = search_space.difference(area)
    
    # Returned search space is one or multiple polygons with float vertices
    # Get all inner points of these polygons considering integer rounding. These are candidates for distress beacon position
    x_candidates = set()
    y_candidates = set()
    if isinstance(search_space, MultiPolygon):
        uncovered_areas = search_space.geoms
    else:  # seach space is a single Polygon
        uncovered_areas = [search_space]

    for polygon in uncovered_areas:
        for x, y in polygon.exterior.coords:
            x_candidates = x_candidates.union(set([int(x), int(x)+1, int(x)-1]))
            y_candidates = y_candidates.union(set([int(y), int(y)+1, int(y)-1]))
            candidate_positions = list(product(x_candidates, y_candidates))

    # Check if each candidate position is covered by any sensor
    covered_positions = []
    for pos in candidate_positions:
        for sensor in sensors:
            if sensor.covers(pos):
                covered_positions.append(pos)
                break

    beacon_pos = set(candidate_positions).difference(set(covered_positions)).pop()
    return f"\n\tCandidate positions: {candidate_positions}\n\tBeacon position: {beacon_pos}\n\tPart 2 answer: {beacon_pos[0] * 4000000 + beacon_pos[1]}"

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

