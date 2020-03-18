import bpy
from random import randint

maze = [
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,1,0,1,0,1,0,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,1,0,0,1,0,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,0,1,1,0,1,0,1,0,1,1,0,1,1],
    [1,0,0,1,0,0,0,0,1,0,1,1,0,0,0,0,1],
    [1,1,0,0,0,1,1,0,0,0,1,0,0,1,1,0,1],
    [1,0,0,1,0,1,0,0,1,0,0,1,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
] 

for i, row in enumerate(maze):
    for j, cell in enumerate(row):
        if cell == 1:
            bpy.ops.mesh.primitive_cube_add(location = (i*2,j*2,0))


bpy.ops.mesh.primitive_cube_add(location = (0,2,0))
cube = bpy.data.objects[ bpy.context.object.name ]
frame_number = 0
bpy.context.scene.frame_set(frame_number)
cube.keyframe_insert(data_path = 'location', index = -1)
frame_number += 5

neighs = [
    (-1,0),
    (0,1),
    (1,0),
    (0,-1)
]

rows = len(maze)
cols = len(maze[0])

current = (0,1)
finish = (rows-1, cols-2)
print(finish)
visited = []
track = []
n = 0

while current != finish and n < 100:
    n += 1
    visited.append(current)
    
    cur_neighs = []

    for neigh in neighs:
        if (
            neigh[0] + current[0] in range(0, rows)
            and neigh[1] + current[1] in range(0, cols)
            and maze[neigh[0] + current[0]][neigh[1] + current[1]] != 1
            and (neigh[0] + current[0], neigh[1] + current[1]) not in visited 
        ):
            cur_neighs.append( (neigh[0] + current[0], neigh[1] + current[1]) )
    

    if len(cur_neighs)>0:
        track.append(current)
        current = cur_neighs[randint(0,len(cur_neighs)-1)]
    else:
        current = track.pop() 
    
    bpy.context.scene.frame_set(frame_number)
    cube.location.x = current[0]*2
    cube.location.y = current[1]*2
    cube.keyframe_insert(data_path = 'location', index = -1)
    frame_number += 5