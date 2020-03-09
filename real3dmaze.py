import math
4
maze = [
    [[1,0,0],[1,0,0],[1,1,0],[0,0,0],[0,0,0],[1,0,0],[0,0,1],[1,0,0],[1,1,0],[1,1,1],[1,1,0],[1,0,0],[0,0,0]],
    [[1,0,0],[1,0,0],[1,1,0],[1,1,0],[1,1,1],[1,1,1],[1,1,1],[1,0,0],[1,0,0],[1,1,0],[1,1,0],[1,1,1],[1,0,1]],
    [[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,1],[1,1,1],[1,1,1],[1,1,0],[1,1,0],[1,1,0],[1,1,0],[1,1,1],[1,1,1]]
]


start = (1,0,1)
finish = (1,12,1)

# A cell position is defined by [x][y][z]
# To find a cell's neighbor, we need to check its 26 adjacent cells
# Let's say we have an agent at cell [1][1][1] looking to the right of the maze (in front of him)
# Front : [x][y+1][z], [x][y+1][z+1], [x+1][y+1][z+1], [x+1][y+1][z], [x+1][y+1][z-1], [x][y+1][z-1], [x-1][y+1][z-1], [x-1][y+1][z], [x-1][y+1][z+1]
# Laterals : [x][y][z+1], [x+1][y][z+1], [x+1][y][z], [x+1][y][z-1], [x][y][z-1], [x-1][y][z-1], [x-1][y][z], [x-1][y][z+1]
# Back : [x][y-1][z], [x][y-1][z+1], [x+1][y-1][z+1], [x+1][y-1][z], [x+1][y-1][z-1], [x][y-1][z-1], [x-1][y-1][z-1], [x-1][y-1][z], [x-1][y-1][z+1]

def get_neighbors(x , y , z , X , Y , Z , maze):
    neighs = []
    one_axis = [
        {'pos': ( x,    y,    z+1 ), 'neighs' : [ (x+1,y,z+1), (x-1,y,z+1), (x,y+1,z+1), (x,y-1,z+1) ]},
        {'pos': ( x,    y,    z-1 ), 'neighs' : [ (x+1,y,z-1), (x-1,y,z-1), (x,y+1,z-1), (x,y-1,z-1) ]},
        {'pos': ( x+1,  y,    z   ), 'neighs' : [ (x+1,y+1,z), (x+1,y-1,z), (x+1,y,z+1), (x+1,y,z-1) ]},
        {'pos': ( x-1,  y,    z   ), 'neighs' : [ (x-1,y+1,z), (x-1,y-1,z), (x-1,y,z+1), (x-1,y,z-1) ]},
        {'pos': ( x,    y+1,  z   ), 'neighs' : [ (x+1,y+1,z), (x-1,y+1,z), (x,y+1,z+1), (x,y+1,z-1) ]},
        {'pos': ( x,    y-1,  z   ), 'neighs' : [ (x+1,y-1,z), (x-1,y-1,z), (x,y-1,z+1), (x,y-1,z-1) ]}
    ]

    two_axis = {
        (x+1,y,z+1) : { 'count': 0, 'neighs' : [ (x+1,y+1,z+1), (x+1,y-1,z+1) ] }, 
        (x-1,y,z+1) : { 'count': 0, 'neighs' : [ (x-1,y+1,z+1), (x-1,y-1,z+1) ] },
        (x,y+1,z+1) : { 'count': 0, 'neighs' : [ (x+1,y+1,z+1), (x-1,y+1,z+1) ] },
        (x,y-1,z+1) : { 'count': 0, 'neighs' : [ (x+1,y-1,z+1), (x-1,y-1,z+1) ] },
        (x+1,y,z-1) : { 'count': 0, 'neighs' : [ (x+1,y+1,z-1), (x+1,y-1,z-1) ] },
        (x-1,y,z-1) : { 'count': 0, 'neighs' : [ (x-1,y+1,z-1), (x-1,y-1,z-1) ] },
        (x,y+1,z-1) : { 'count': 0, 'neighs' : [ (x+1,y+1,z-1), (x-1,y+1,z-1) ] },
        (x,y-1,z-1) : { 'count': 0, 'neighs' : [ (x+1,y-1,z-1), (x-1,y-1,z-1) ] },
        (x+1,y+1,z) : { 'count': 0, 'neighs' : [ (x+1,y+1,z+1), (x+1,y+1,z-1) ] },
        (x+1,y-1,z) : { 'count': 0, 'neighs' : [ (x+1,y-1,z+1), (x+1,y-1,z-1) ] },
        (x-1,y+1,z) : { 'count': 0, 'neighs' : [ (x-1,y+1,z+1), (x-1,y+1,z-1) ] },
        (x-1,y-1,z) : { 'count': 0, 'neighs' : [ (x-1,y-1,z+1), (x-1,y-1,z-1) ] }
    }

    three_axis = {
        (x+1,y+1,z+1) : 0,
        (x+1,y-1,z+1) : 0,
        (x-1,y+1,z+1) : 0,
        (x-1,y-1,z+1) : 0,
        (x+1,y+1,z-1) : 0,
        (x+1,y-1,z-1) : 0,
        (x-1,y+1,z-1) : 0,
        (x-1,y-1,z-1) : 0
    }


    for cell in one_axis:
        if (cell['pos'][0] in range(0,X) and
        cell['pos'][1] in range(0,Y) and
        cell['pos'][2] in range(0,Z) and
        maze[cell['pos'][0]][cell['pos'][1]][cell['pos'][2]] != 1):

            neighs.append(cell['pos'])

            for neigh in cell['neighs']:
                if (neigh[0] in range(0,X) and
                neigh[1] in range(0,Y) and
                neigh[2] in range(0,Z) and
                maze[neigh[0]][neigh[1]][neigh[2]] != 1):
                    two_axis[neigh]['count'] += 1

    for cell in two_axis:
        if two_axis[cell]['count'] == 2:
            neighs.append(cell)
            for neigh in two_axis[cell]['neighs']:
                if (neigh[0] in range(0,X) and
                neigh[1] in range(0,Y) and
                neigh[2] in range(0,Z) and
                maze[neigh[0]][neigh[1]][neigh[2]] != 1):
                    three_axis[neigh] += 1

    for cell in three_axis:
        if three_axis[cell] == 3:
            neighs.append(cell)
    
    return neighs

def make_graph(maze,finish):
    graph = {}
    X = len( maze )
    Y = len( maze[ 0 ] )
    Z = len( maze[ 0 ][ 0 ] )
    
    for x in range( 0 , X ):
        for y in range( 0 , Y ):
            for z in range( 0 , Z ):
                graph[(x,y,z)] = {
                    'pos' : ( x , y , z ),
                    'g_cost' : float('inf'),
                    'h_cost' : round( math.sqrt( ( finish[0]-x )**2 + ( finish[1]-y )**2 + ( finish[2]-z )**2 ) * 10 , 0 ),
                    'f_cost' : float('inf'),
                    'visited' : False,
                    'parent' : None,
                    'neighbors' : get_neighbors( x , y , z , X , Y , Z , maze )
                }

    return graph

def a_star(graph, start, finish):
    
    graph[ ( start ) ][ 'g_cost' ] = 0
    graph[ ( start ) ][ 'f_cost' ] = graph[ ( start ) ][ 'h_cost' ]

    open = [ graph[ ( start ) ] ]

    current = None

    while current != graph[ ( finish ) ]:
        current = min( open, key = lambda cell: cell['f_cost'] )
        open.remove( current )
        current[ 'visited' ] = True

        for neighbor in current['neighbors']:
            
            if graph[neighbor]['visited'] == True:
                continue

            path_to_neigh = current[ 'g_cost' ] + round( 
                math.sqrt( 
                    ( neighbor[0] - current['pos'][0] )**2 + ( neighbor[1] - current['pos'][1] )**2 + ( neighbor[2] - current['pos'][2] )**2 ) * 10 
                , 0 )
            neighbor = graph[neighbor]

            print(path_to_neigh)
            if neighbor not in open or neighbor[ 'g_cost' ] > path_to_neigh:
                neighbor[ 'h_cost' ] = round( 
                    math.sqrt( 
                        ( finish[0] - neighbor['pos'][0] )**2 + ( finish[1] - neighbor['pos'][1] )**2 + ( finish[2] - neighbor['pos'][2] )**2 ) * 10 
                    , 0 )
                neighbor[ 'g_cost' ] = path_to_neigh
                neighbor[ 'f_cost']
                neighbor['parent'] = current['pos']

                if neighbor not in open:
                    open.append(neighbor)

    return graph



graph = a_star( make_graph( maze, finish ) , start , finish )
current = graph[finish]
track = []
n = 0 

while current['parent'] != None and n < 15:
    n+=1
    track.insert(0, current['pos'])
    current = graph[ current[ 'parent' ] ]
track.insert( 0, graph[ ( 1 , 0 , 1 ) ][ 'pos' ] )

print( track )
