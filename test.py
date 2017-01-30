import tsp_optimal as opt
from lib import read_matrix_from_csv, generate_points, calculate_distance_matrix, print_route, calc_route_length, run_matlab_script, write_matrix_to_csv, create_tsplib_file
import tsp_heuristics

def main():
    point_list = generate_points(5, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    #tour = tsp_heuristics.mst_heuristic_matlab(matrix)
    tour = opt.solve_optimal_coin_pulp(matrix)
    
if __name__ == '__main__':
    main()
