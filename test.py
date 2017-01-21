import tsp_optimal as opt
from lib import read_matrix_from_csv, generate_points, calculate_distance_matrix, print_route, calc_route_length, run_matlab_script, write_matrix_to_csv
import tsp_heuristics

def main():
    better_list = []
    for i in range(30):
        point_list = generate_points(50, 0, 10)
        matrix = calculate_distance_matrix(point_list)
        ni = tsp_heuristics.nearest_insertion(matrix)
        nn = tsp_heuristics.nearest_neighbour(matrix)
        if ni != nn:
            better_list.append('ni' if ni < nn else 'nn')
        print('nearest insertion', calc_route_length(ni, matrix))
        print('nearest neighbour', calc_route_length(nn, matrix))
        print()
    print('Nearest neighbour besser: ', sum([1 for i in better_list if i == 'nn']))
    print('Nearest insertion besser: ', sum([1 for i in better_list if i == 'ni']))
    #tsp_heuristics.test_is_cycle()
    
    
if __name__ == '__main__':
    main()