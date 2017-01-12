import tsp_optimal as opt
from lib import generate_points, calculate_distance_matrix, print_route, calc_route_length

def main():
    point_list = generate_points(5, 0, 10)
    matrix = calculate_distance_matrix(point_list)
    
    route = opt.solve_optimal_gurobi(matrix)
    #route = opt.solve_optimal_lpsolve(matrix)
    print(route)
    
if __name__ == '__main__':
    main()