import tsp_optimal as opt
from lib import read_matrix_from_csv, generate_points, calculate_distance_matrix, print_route, calc_route_length, run_matlab_script, write_matrix_to_csv, create_tsplib_file
import tsp_heuristics

def main():
    point_list = generate_points(50, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    tour = tsp_heuristics.multi_fragment(matrix)
    #create_tsplib_file('tspfile.tsp', point_list)
    #tour = opt.solve_optimal(matrix, point_list)
    print(tour)
    
if __name__ == '__main__':
    main()
