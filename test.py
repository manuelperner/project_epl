import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route, calc_route_length, run_matlab_script, write_matrix_to_csv

def main():
    point_list = generate_points(5, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    write_matrix_to_csv(matrix, 'matrix.csv')
    my_str = run_matlab_script('mst_heuristic.m')
    print(my_str)
    
if __name__ == '__main__':
    main()