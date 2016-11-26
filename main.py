import random

import tsp_heuristics

def main():
    # tsp_heuristics.nearest_neighbour
    point_list = generate_points(5, 0, 10)
    distance_matrix = calculate_distance_matrix(point_list)
    print('Points: ', point_list)
    print()
    
    nn_solution = tsp_heuristics.nearest_neighbour(distance_matrix)
    print('Nearest Neighbour:', nn_solution)

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
    
main()