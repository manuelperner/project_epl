import random
import matplotlib.pyplot as plt

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


def print_matrix(matrix):
    for line in matrix:
        print(', '.join('{:5.2f}'.format(item) for item in line))


def find_nearest(distance_matrix, v, unvisited):
    """Searches for the point with the nearest distance from vertex v to another one within the unvisited"""
    assert len(unvisited) > 0
    nearest = None
    for u in unvisited:
        if nearest is None:
            nearest = u
        if distance_matrix[v][u] < distance_matrix[v][nearest]:
            nearest = u
    return nearest

def tsp_nearest_neighbour(distance_matrix):
    """Returns a NN route (a list of indices: the first one is the start start index of the route, the last one is
    the last vistited point in the route
    """
    route = [0]  # start with the depot
    unvisited = set(range(len(distance_matrix))) - set(route)
    while len(unvisited) > 0:
        v = route[-1]
        nearest = find_nearest(distance_matrix, v, unvisited)
        route.append(nearest)
        unvisited -= set([nearest])
    route.append(route[0])  # first point should be last point
    return route


def main():
    points = generate_points(50, 0, 10)
    distance_matrix = calculate_distance_matrix(points)
    print_matrix(distance_matrix)
    tsp_route = tsp_nearest_neighbour(distance_matrix)
    # draw all points:
    x_list = [x for x,y in points]
    y_list = [y for x,y in points]
    plt.plot(x_list, y_list, marker='o', linestyle='', color='green')

    # draw nearest neighbour route:
    tsp_x = [points[i][0] for i in tsp_route]
    tsp_y = [points[i][1] for i in tsp_route]
    plt.plot(tsp_x, tsp_y)

    # draw the start point:
    plt.plot( [tsp_x[0]], [tsp_y[0]], marker='o', alpha=1, linestyle='', color='red', markersize=15)
    plt.ylim(-1, 11)
    plt.xlim(-1, 11)
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()