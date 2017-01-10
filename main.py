import tsp_heuristics as heur
import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route

def main():
    point_list = generate_points(20, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    print('Random Points: ', point_list)
    print()
    
    nn_solution = heur.nearest_neighbour(matrix)
    opt_solution = opt.solve_optimal(matrix)
    
    print('Nearest Neighbour Solution:')
    print_route(nn_solution, matrix)
    
    print('Optimal Solution:')
    print_route(opt_solution, matrix)

def plot():
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