import math
import numpy as np
rot_angles_rad = [math.radians(90*i) for i in range(4)]

#for i in rot_angles_rad:
#    print(int(math.cos(i)))

# https://en.wikipedia.org/wiki/Rotation_matrix - General rotation matrix = Rx.Ry.Rz
# Rotate each axis x,y,z by (0,90,180,270) degrees => 4*4*4 = 64 combinations; Deduplicate => 24 unique rotations
rot_matrix_data = []
for x in rot_angles_rad:
    rx = np.array([[1, 0, 0],[0, math.cos(x), -math.sin(x)],[0, math.sin(x), math.cos(x)]], dtype=np.int8)
    for y in rot_angles_rad:
        ry = np.array([[math.cos(y), 0, math.sin(y)],[0, 1, 0],[-math.sin(y), 0, math.cos(y)]], dtype=np.int8)
        for z in rot_angles_rad:
            rz = np.array([[math.cos(z), -math.sin(z), 0],[math.sin(z), math.cos(z), 0],[0, 0, 1]], dtype=np.int8)
            rot_matrix = rx.dot(ry).dot(rz) # Rx.Ry.Rz
            rot_matrix_data.append(tuple(map(tuple, rot_matrix))) # Convert array to tuple of tuple to deduplicate

rot_matrices = [np.array(r, dtype=np.int8) for r in set(rot_matrix_data)]
print(len(rot_matrices))

points = np.array([
    [-1,-1,1],
    [-2,-2,2],
    [-3,-3,3],
    [-2,-3,1],
    [5,6,-4],
    [8,0,7]
    ])

rotated_point = points.dot(rot_matrices[1])
print(rotated_point)
rotated_point = np.array(sorted(rotated_point, key=lambda x: (x[0], x[1], x[2])))
print(rotated_point)

# Count occurence of each row in np array
a = np.array([
    [-1,-1,1],
    [-2,-2,2],
    [8,0,7],
    [8,0,7],
    [5,6,-4],
    [8,0,7]
    ])

unq, cnt = np.unique(a, axis=0, return_counts=True)
print(unq, cnt)

a = a + np.array([1,1,1])
print(a)