import matplotlib.pyplot as plt
import numpy as np

import tsp_heuristics as heur
import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route, calc_route_length

def main():
    point_list = generate_points(30, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    
    data = {
        'nn_route' : heur.nearest_neighbour(matrix),
        'fcfs': heur.first_come_first_serve(matrix),
        'opt_solution' : opt.solve_optimal(matrix),
        'matrix' : matrix,
        'points' : point_list}
    
    plot(data)
    

def plot(data):
    fig, axes = plt.subplots(2, 2, sharex='col', sharey='row')
    axes = tuple(np.array(axes).flatten())
    ax1, ax2, ax3, ax4 = axes
    # draw all points on all axes:
    x_list = [x for x,y in data['points']]
    y_list = [y for x,y in data['points']]
    for ax in axes:
        ax.plot(x_list, y_list, marker='o', linestyle='', color='green')
    
    draw_route(data['opt_solution'], ax1, 'Optimal Solution', data)
    draw_route(data['nn_route'], ax2, 'Nearest Neighbour', data)
    draw_route(data['fcfs'], ax3, 'FirstComeFirstServe', data)
    
    plt.ylim(-1, 11)
    plt.xlim(-1, 11)
    plt.grid()
    plt.legend()
    plt.show()
    
def draw_route(route, axis, label, data):
    tsp_x = [data['points'][i][0] for i in route]
    tsp_y = [data['points'][i][1] for i in route]
    # also close the route:
    tsp_x.append(tsp_x[0])
    tsp_y.append(tsp_y[0])
    route_length = calc_route_length(route, data['matrix'])
    axis.plot(tsp_x, tsp_y, label=label)
    axis.set_title('{} (${}$={:.2f})'.format(label, 'Dist_{Total}', route_length))


if __name__ == '__main__':
    main()