import datetime
import numpy as np

exec_part = 2 # which part to execute
exec_test_case = 0 # -1 = all test inputs, n = n_th test input; 0 = real puzzle input

# Puzzle input
with open('input/input_test22.txt') as f:
    INPUT_TEST = f.read()

with open('input/input22.txt') as f:
    INPUT = f.read()   

def parse_input(input):
    steps = []
    for r in input.split('\n'):
        switch, cub_pos_txt = r.replace('x=','').replace('y=','').replace('z=','').split(' ')
        switch_code = 1 if switch == 'on' else 0
        cube_pos = tuple([tuple(list(map(int, c.split('..')))) for c in cub_pos_txt.split(',')])
        steps.append((switch_code, cube_pos))
    return steps

def part1(input):
    cubes = np.zeros([101,101,101], dtype=np.int8)
    for switch, cube_pos in input:
        x1, x2, y1, y2, z1, z2 = [i + 50 for c in cube_pos for i in c]
        if not (np.all(np.array([p in range (0, 102) for p in [x1, x2, y1, y2, z1, z2]]))):
            continue
        cubes[x1 : x2 + 1, y1 : y2 + 1, z1 : z2 + 1] = switch
    return np.count_nonzero(cubes == 1)

def range_overlap(r1, r2):
    ((x1, x2), (y1, y2)) = r1, r2
    if x2 < y1 or x1 > y2: 
        return None
    return tuple(sorted([x1, x2, y1, y2])[1:-1])

def intersect_cube(cube1, cube2):
    intersect =  tuple([range_overlap(*p) for p in zip (cube1, cube2)])
    if None in intersect:
        return None
    return intersect

# Split range r(x,y) by a threshold t
def split_range(r, t):
    x, y = r
    if t <= x:
        return (None, r)
    elif t > y:
        return (r, None)
    else:
        return ((x, t-1), (t,y))
        #return ((x, t), (t+1,y))

# Cut a cube by a 2d plane that is parallel with 2/3 axes, for example x = 15
# Returns (new cube, leftover of original cube)
def plane_cut(ax, value, cube):
    if cube is None:
        return (None, None)
    (x_range, y_range, z_range) = cube
    if(ax == 'x'):
        x_split = split_range(x_range, value)
        cube1, cube2 = (x_split[0], y_range, z_range), (x_split[1], y_range, z_range)
    elif(ax == 'y'):
        y_split = split_range(y_range, value)
        cube1, cube2 = (x_range, y_split[0], z_range), (x_range, y_split[1], z_range)
    else:
        z_split = split_range(z_range, value)
        cube1, cube2 = (x_range, y_range, z_split[0]), (x_range, y_range, z_split[1])
    if None in cube1: cube1 = None
    if None in cube2: cube2 = None
    return (cube1, cube2)

def part2(input):
    #input = [t for t in input if t[1][0][0] in range(-50,50)]
    cubes = []
    for (switch, cube) in input:
        # See how the new cube interacts with existing cubes
        new_cubes = []
        for c in cubes:
            # Find intersect of the new cube and existing cube 
            intersect = intersect_cube(cube, c)
            #print('intersect', intersect) #***********
            if intersect is None:
                new_cubes.append(c)
                continue
            ((x1, x2), (y1, y2), (z1, z2)) = intersect
            # Cut existing cube by 6 planes of the intersect cube
            #print('cube', c)
            splitted_cube1, left_over_cube = plane_cut('x', x1, c)
            #print('leftover1', left_over_cube) #***********
            left_over_cube, splitted_cube2 = plane_cut('x', x2+1, left_over_cube)
            #print('leftover2', left_over_cube) #***********
            splitted_cube3, left_over_cube = plane_cut('y', y1, left_over_cube)
            #print('leftover3', left_over_cube) #***********
            left_over_cube, splitted_cube4 = plane_cut('y', y2+1, left_over_cube)
            #print('leftover4', left_over_cube) #***********
            splitted_cube5, left_over_cube = plane_cut('z', z1, left_over_cube)
            #print('leftover5', left_over_cube) #***********
            left_over_cube, splitted_cube6 = plane_cut('z', z2+1, left_over_cube)
            #print('leftover6', left_over_cube) #***********
            #print('leftover6 == intersect:', left_over_cube == intersect)
            new_cubes.extend([i for i in [splitted_cube1, splitted_cube2, splitted_cube3, splitted_cube4, splitted_cube5, splitted_cube6] if i is not None])
        
        cubes = new_cubes.copy()
        if(switch == 1):
            cubes.append(cube)
    
    cell_count = 0
    for c in cubes:
        ((x1, x2), (y1, y2), (z1, z2)) = c
        cell_count += (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
    return cell_count

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

