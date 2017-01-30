import matplotlib.pyplot as plt
import numpy as np

import tsp_heuristics as heur
import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route, calc_route_length, write_matrix_to_csv

def main():
    point_list = generate_points(20, 30, 100)
    matrix = calculate_distance_matrix(point_list)
    data = {
        'nn_route' : heur.nearest_neighbour(matrix),
        'fcfs': heur.first_come_first_serve(matrix),
        'ni_route' : heur.nearest_insertion(matrix),
        'ch_route' : heur.cheapest_insertion(matrix),
        'mst_route' : heur.mst_heuristic(matrix),
        'mult_route' : heur.multi_fragment(matrix),
        'opt_solution' : opt.solve_optimal(matrix, point_list),
        'matrix' : matrix,
        'points' : point_list}
    data['opt_length'] = calc_route_length(data['opt_solution'], matrix)
    plot(data)
    

def plot(data):
    fig, axes = plt.subplots(3, 2, sharex='col', sharey='row')
    axes = tuple(np.array(axes).flatten())
    ax1, ax2, ax3, ax4, ax5, ax6 = axes
    # draw all points on all axes:
    x_list = [x for x,y in data['points']]
    y_list = [y for x,y in data['points']]
    for ax in axes:
        ax.plot(x_list, y_list, marker='o', linestyle='', color='green')
    
    draw_route(data['opt_solution'], ax1, 'Optimal Solution', data)
    draw_route(data['nn_route'], ax2, 'Nearest Neighbour', data)
    draw_route(data['ni_route'], ax3, 'Nearest Insertion', data),
    draw_route(data['mst_route'], ax4, 'MST Heuristic', data),
    draw_route(data['mult_route'], ax5, 'Multi Fragment', data),
    draw_route(data['ch_route'][0], ax6, 'Cheapest Insertion, costs={:.2f}'.format(data['ch_route'][1]), data)
    
    #plt.ylim(-1, 11)
    #plt.xlim(-1, 11)
    #plt.grid()
    #plt.legend()
    test
    plt.show()
    
def draw_route(route, axis, label, data):
    tsp_x = [data['points'][i][0] for i in route]
    tsp_y = [data['points'][i][1] for i in route]
    # also close the route:
    tsp_x.append(tsp_x[0])
    tsp_y.append(tsp_y[0])
    route_length = calc_route_length(route, data['matrix'])
    if label != 'Optimal Solution':
        error = (route_length / data['opt_length'])-1
        error_str = ', Error = {:.2f}%'.format(error*100)
    else:
        error_str = ''
    axis.plot(tsp_x, tsp_y, label=label)
    axis.set_title('{} (${}$={:.2f}{})'.format(label, 'Dist_{Total}', route_length, error_str))


if __name__ == '__main__':
    main()
