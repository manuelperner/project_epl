import tsp_optimal as opt
from lib import read_matrix_from_csv, generate_points, calculate_distance_matrix, print_route, calc_route_length, run_matlab_script, write_matrix_to_csv
import tsp_heuristics

def main():
    point_list = generate_points(50, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    tsp_heuristics.mst_heuristic(matrix)
    
    
if __name__ == '__main__':
    main()