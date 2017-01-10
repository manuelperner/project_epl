import random

def print_matrix(matrix):
    for line in matrix:
        print(', '.join('{:5.2f}'.format(item) for item in line))
        
def calculate_distance_matrix(points):
    """returns a distance matrix (euclidean distance).
    points: a list of x,y tuples"""
    n = len(points)
    matrix = [[None for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            # calculate distance between point n and m
            point_1 = points[i]
            point_2 = points[j]
            #matrix[i][j] = round(((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**(1/2), 2)
            matrix[i][j] = round(((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**(1/2), 2)
    return matrix
    
def calc_route_length(route, matrix):
    route = route[:] + [route[0]]
    length = 0
    for act in range(1, len(route)):
        prev = act - 1
        length += matrix[route[prev]][route[act]]
    return length
    
def print_route(route, matrix):
    route_incl = route[:] + [route[0]]
    route_str = ' -> '.join(map(str, route_incl))
    dist = calc_route_length(route, matrix)
    print('{} [dist: {:.2f}]'.format(route_str, dist))

def generate_points(number, min, max):
    """generates `number` random points in a x,y field - limited by `min` and max"""
    l = []
    for i in range(number):
        x = random.random()
        y = random.random()
        x = round((max-min) * x + min, 2)
        y = round((max - min) * y + min, 2)
        l.append((x,y))
    return l