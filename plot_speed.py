from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import random

import tsp_heuristics as heur
import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route

MIN_INSTANCE_SIZE = 3
MAX_INSTANCE_SIZE = 4
STEP = 1
SIMULATIONS = 4

def main():
    data = []
    instance_sizes = list(range(MIN_INSTANCE_SIZE, MAX_INSTANCE_SIZE+1, STEP))
    for i in range(SIMULATIONS):
        sim_data = {
            'instance_size': [],
            'nearest_neighbour_time': [],
            'optimal_gurobi_time': []
        }
        
        for instance_size in instance_sizes:
            print(instance_size)
            # create test instance:
            sim_data['instance_size'].append(instance_size)
            print(instance_size)
            point_list = generate_points(instance_size, 0, 10)
            matrix = calculate_distance_matrix(point_list)
            
            time, route = test_algorithm(matrix, 'nearest_neighbour')
            sim_data['nearest_neighbour_time'].append(time)
            
            time, route = test_algorithm(matrix, 'optimal')
            sim_data['optimal_gurobi_time'].append(time)
            
        data.append(sim_data)
    
    avg_nn = [avg([data[sim]['nearest_neighbour_time'][ins_size_ind] for sim in range(SIMULATIONS)]) for ins_size_ind in range(len(instance_sizes))]
    avg_opt = [avg([data[sim]['optimal_gurobi_time'][ins_size_ind] for sim in range(SIMULATIONS)]) for ins_size_ind in range(len(instance_sizes))]
    
    avg_data = {
        'instance_size' : data[0]['instance_size'],
        'nearest_neighbour_time' : avg_nn,
        'optimal_gurobi_time' : avg_opt
        }
    plot(avg_data)
    
def avg(l):
    return sum(l) / len(l)

def test_algorithm(matrix, method):
    time_start = datetime.now()
    if method == 'optimal':
        route = opt.solve_optimal(matrix)
    elif method == 'nearest_neighbour':
        route = heur.nearest_neighbour(matrix)
    time_end = datetime.now()
    delta = (time_end - time_start)
    delta = delta.seconds + (delta.microseconds / (1000*1000))
    return delta, route

def plot(data):
    fig, ax1 = plt.subplots()
    sns.set_palette('RdGy')
    
    size = data['instance_size']
    ax1.plot(size, data['nearest_neighbour_time'], label='Nearest Neighbour time')
    ax1.legend(loc='upper left')
    ax1.set_xlabel('Instance size')
    ax1.set_ylabel('Time [s]')
    
    ax2 = ax1.twinx()
    ax2.plot(size, data['optimal_gurobi_time'], label='Solver time')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Time [s]')
    plt.show()

if __name__ == '__main__':
    main()