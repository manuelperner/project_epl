from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import random
import json

import tsp_heuristics as heur
import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route

MIN_INSTANCE_SIZE = 5
MAX_INSTANCE_SIZE = 40
STEP = 5
SIMULATIONS = 50

SIM_FILENAME = str(datetime.now()).replace(' ', '_') + '.json'

def append_data_to_sim_file(filename, data):
    with open(filename, 'a') as f:
        f.write(json.dumps(data, sort_keys=True, indent=None))
        f.write('\n')

def main():
    data = []
    instance_sizes = list(range(MIN_INSTANCE_SIZE, MAX_INSTANCE_SIZE+1, STEP))
    for i in range(SIMULATIONS):
        sim_data = {
            'instance_size': [],
            'nearest_neighbour_time': [],
            'optimal_concorde_time': [],
            'optimal_gurobi_time' : [],
            'optimal_coin_time' : [],
        }
        
        for instance_size in instance_sizes:
            # create test instance:
            sim_data['instance_size'].append(instance_size)
            print(i, instance_size)
            point_list = generate_points(instance_size, 0, 10)
            matrix = calculate_distance_matrix(point_list)
            
            #time, route = test_algorithm(matrix, point_list, 'nearest_neighbour')
            #sim_data['nearest_neighbour_time'].append(time)
            
            conc_time, route = test_algorithm(matrix, point_list, 'optimal_concorde')
            sim_data['optimal_concorde_time'].append(conc_time)
            
            gur_time, route = test_algorithm(matrix, point_list, 'optimal_gurobi')
            sim_data['optimal_gurobi_time'].append(gur_time)
            
            coin_time, route = test_algorithm(matrix, point_list, 'optimal_coin')
            sim_data['optimal_coin_time'].append(coin_time)
            
            act_data = {'size' : instance_size, 'conc_time' : conc_time, 'gur_time' : gur_time, 'coin_time' : coin_time, 'time' : str(datetime.now())}
            append_data_to_sim_file(SIM_FILENAME, act_data)
            
        data.append(sim_data)
    
    #avg_nn = [avg([data[sim]['nearest_neighbour_time'][ins_size_ind] for sim in range(SIMULATIONS)]) for ins_size_ind in range(len(instance_sizes))]
    avg_conc = [avg([data[sim]['optimal_concorde_time'][ins_size_ind] for sim in range(SIMULATIONS)]) for ins_size_ind in range(len(instance_sizes))]
    avg_gur = [avg([data[sim]['optimal_gurobi_time'][ins_size_ind] for sim in range(SIMULATIONS)]) for ins_size_ind in range(len(instance_sizes))]
    avg_coin = [avg([data[sim]['optimal_coin_time'][ins_size_ind] for sim in range(SIMULATIONS)]) for ins_size_ind in range(len(instance_sizes))]
    
    avg_data = {
        'instance_size' : data[0]['instance_size'],
        #'nearest_neighbour_time' : avg_nn,
        'optimal_concorde_time' : avg_conc,
        'optimal_gurobi_time' : avg_gur,
        'optimal_coin_time' : avg_coin
        }
    plot(avg_data)
    
def avg(l):
    return sum(l) / len(l)

def test_algorithm(matrix, point_list, method):
    time_start = datetime.now()
    if method == 'optimal_concorde':
        route = opt.solve_optimal_concorde(point_list)
    elif method == 'optimal_gurobi':
        route = opt.solve_optimal_gurobi(matrix)
    elif method == 'optimal_coin':
        route = opt.solve_optimal_coin_pulp(matrix)
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
    ax1.plot(size, data['optimal_concorde_time'], label='Concorde optimal time')
    ax1.legend(loc='upper left')
    ax1.set_xlabel('Instance size')
    ax1.set_ylabel('Time [s] Concorde')
    
    ax2 = ax1.twinx()
    ax2.plot(size, data['optimal_gurobi_time'], label='Gurobi optimal time')
    ax2.plot(size, data['optimal_coin_time'], label='COIN OR optimal time')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Time [s] ILP')
    plt.title('Average calculation time of {} random instances each instance size'.format(SIMULATIONS))
    plt.show()

if __name__ == '__main__':
    main()
