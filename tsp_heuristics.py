from lib import calc_route_length, print_route

def nearest_neighbour(matrix):
    """Returns a NN route (a list of indices: the first one is the start start index of the route, the last one is
    the last vistited point in the route
    """
    all_routes = []
    # calculate the nearest neighbour for each start point
    for v in range(len(matrix)):
        all_routes.append(__nearest_neighbour_fixed_start(matrix, v))
    # return the best route of all:
    return min(all_routes, key=lambda route: calc_route_length(route, matrix))
     
def nearest_insertion(matrix):
    raise NotImplementedError()
    
def cheapest_insertion(matrix):
    raise NotImplementedError()
    
def mst_heuristic(matrix):
    raise NotImplementedError()
    
def multi_fragment(matrix):
    raise NotImplementedError()
    
def __nearest_neighbour_fixed_start(matrix, start):
    """Returns a NN route (a list of indices: the first one is the start start index of the route, the last one is
    the last vistited point in the route
    """
    route = [start]  # a fixed start point
    unvisited = set(range(len(matrix))) - set(route)
    while len(unvisited) > 0:
        v = route[-1]
        nearest = __find_nearest(matrix, v, unvisited)
        route.append(nearest)
        unvisited -= set([nearest])
    return route
    
def __find_nearest(distance_matrix, v, unvisited):
    """Searches for the point with the nearest distance from vertex v to another one within the unvisited"""
    assert len(unvisited) > 0
    nearest = None
    for u in unvisited:
        if nearest is None:
            nearest = u
        if distance_matrix[v][u] < distance_matrix[v][nearest]:
            nearest = u
    return nearest