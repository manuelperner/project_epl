from itertools import chain

from lib import calc_route_length, create_matrix, write_matrix_to_csv, run_matlab_script
from lib import print_matrix, print_route


def first_come_first_serve(matrix):
    return list(range(len(matrix)))

def mst_heuristic(matrix):
    try:
        return mst_heuristic_matlab(matrix)
    except:
        print('warning: matlab not installed')
        return mst_heuristic_python(matrix)

def mst_heuristic_matlab(matrix):
    write_matrix_to_csv(matrix, 'matrix.csv')
    route = run_matlab_script('Kruskal.m')
    route = list(map(int, route.strip().split(',')))
    return route
    
def mst_heuristic_python(matrix):
    # get mst graph
    mst_graph = _kruskal(matrix)
    # create an eulerian graph by double all edges:
    graph = []
    for edge in mst_graph:
        reversed_edge = {'from' : edge['to'], 'to': edge['from'], 'dist' : edge['dist']}
        graph.append(edge)
        graph.append(reversed_edge)
    # create tour
    path = __get_hierholzer_path(graph, 0)
    # remove doubled entries
    tours = [__mst_tour_from_hierholzer(path, start_point) for start_point in range(len(path))]
    tours = [(calc_route_length(tour, matrix), tour) for tour in tours]
    return min(tours, key=lambda k: k[0])[1]
    
def __mst_tour_from_hierholzer(path, start_point):
    tour = []
    for vertex in chain(path[start_point:], path[:start_point]):
        if vertex not in tour:
            tour.append(vertex)
    return tour
    
def __get_hierholzer_path(edges, start_point):
    # create a dict of of vertices having all adjacent edges stored as values
    vertices = {}
    for edge in edges:
        vertex = edge['from']
        adj = vertices.get(vertex, [])
        adj.append(edge)
        vertices[vertex] = adj
    
    forward_stack = []
    backtrack_stack = []
    
    e = __next_unvisited_edge(start_point, vertices)
    while e is not None:
        e['visited'] = True
        forward_stack.append(e)
        e = __next_unvisited_edge(e['to'], vertices)
    
    while len(forward_stack) > 0:
        e = forward_stack.pop()
        backtrack_stack.append(e)
        e = __next_unvisited_edge(e['from'], vertices)
        while e is not None:
            e['visited'] = True
            forward_stack.append(e)
            e = __next_unvisited_edge(e['to'], vertices)
    path = [edge['from'] for edge in reversed(backtrack_stack)]
    return path
    
def __next_unvisited_edge(vertex, vertices):
    """Helper function of __get_hierholzer_path"""
    for edge in vertices[vertex]:
        assert edge['from'] == vertex
        if not 'visited' in edge or not edge['visited']:
            return edge
    return None
    
def multi_fragment(matrix):
    edges = _get_edge_list_from_matrix(matrix)
    # sort edges
    edges.sort(key=lambda d: d['dist'], reverse=True)
    # create a cycle free graph where all vertices have max degree of 2
    graph = []
    vertex_degree = {i: 0 for i in range(len(matrix))}
    while len(edges) > 0:
        shortest_edge = edges.pop()
        # check vertex degree from and to
        from_vertex, to_vertex = shortest_edge['from'], shortest_edge['to']
        if vertex_degree[from_vertex] == 2 or vertex_degree[to_vertex] == 2:
            continue
        # check subcycles
        new_graph = graph + [shortest_edge]
        if _is_cycle(new_graph):
            continue
        else:
            graph = new_graph
        # update graph and vertex degrees
        vertex_degree[from_vertex] += 1; vertex_degree[to_vertex] += 1
    tour = _multi_fragment_build_tour(graph, vertex_degree)
    return tour
    
def _multi_fragment_build_tour(graph, vertex_degree):
    # perfect, we now have to vertices where degree = 1, select one of them
    vertex_neighbours = [[] for _ in vertex_degree]
    for edge in graph:
        vertex_neighbours[edge['from']].append(edge['to'])
        vertex_neighbours[edge['to']].append(edge['from'])
    # find start_edge
    for vert, neighbrs in enumerate(vertex_neighbours):
        if len(neighbrs) == 1:
            start = vert
            break
    tour = [start]
    prev = start
    # now build the tour
    while len(tour) < len(vertex_degree):
        next = vertex_neighbours[prev].pop()
        if len(tour) > 1 and next == tour[-2]:
            next = vertex_neighbours[prev].pop()
        tour.append(next)
        prev = next
    return tour

def _get_edge_list_from_matrix(matrix):
    n = len(matrix)
    # create edges
    edges = list()
    for i in range(n-1):
        for j in range(i+1, n):
            edge = {'from' : i, 'to': j, 'dist' : matrix[i][j]}
            edges.append(edge)
    return edges
    
def _kruskal(matrix):
    """ Returns a list of edges that spans a minimum spaning tree """
    edges = _get_edge_list_from_matrix(matrix)
    # sort edges
    edges.sort(key=lambda d: d['dist'], reverse=True)
    # create a cycle free graph:
    graph = []
    while len(edges) > 0:
        # find the shortest edge in list:
        shortest_edge = edges.pop()
        new_graph = graph + [shortest_edge]
        if not _is_cycle(new_graph):
            graph = new_graph
    return graph
    
def _is_cycle(graph):
    all_vertices = set()
    for edge in graph:
        all_vertices.add(edge['from'])
        all_vertices.add(edge['to'])
    visited = set()
    for i in all_vertices:
        if i not in visited:
            if _is_cycle_start_point(graph, i, visited):
                return True
    return False
  
def _is_cycle_start_point(graph, start_point, visited):
    """ Checks if a given list of edges has a cycle - returns True if a cycle exists"""
    def explore(node_nr, parent_nr):
        #print('Node_nr: {}, parent_nr: {}'.format(node_nr, parent_nr))
        if node_nr in visited:
            return True
        else:
            visited.add(node_nr)
            # search all neighbours
            neighbours = []
            for edge in graph:
                neighbour = None
                if edge['from'] == node_nr:
                    neighbour = edge['to']
                elif edge['to'] == node_nr:
                    neighbour = edge['from']
                if neighbour is not None and neighbour != parent_nr:
                    neighbours.append(neighbour)
            for u in neighbours:
                if explore(u, node_nr):
                    return True
            return False
    is_cycle = explore(start_point, None)
    return is_cycle

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
    
def nearest_insertion(matrix):
    tours = []
    for i in range(len(matrix)):
        tours.append(__nearest_insertion_fixed_start(matrix, i))
    return min(tours, key=lambda k: calc_route_length(k, matrix))
     
def __nearest_insertion_fixed_start(matrix, start_point):
    n = len(matrix)
    tour = [start_point]
    while len(tour) < n:
        all_nearest = []
        # find nearest:
        for tour_point in tour:
            possible_neighbours = [(i, val) for i, val in enumerate(matrix[tour_point]) if i not in tour]
            nearest_to_point = min(possible_neighbours, key=lambda k: k[1])
            all_nearest.append(nearest_to_point)
        next_point = min(all_nearest, key= lambda i: i[1])
        # find best insert position:
        all_possible_tours = []
        for pos in range(len(tour)):
            possible_tour = tour[:pos+1] + [next_point[0]] + tour[pos+1:]
            length = calc_route_length(possible_tour, matrix)
            all_possible_tours.append( [possible_tour, length])
        best_tour = min(all_possible_tours, key=lambda k: k[1])
        tour = best_tour[0]
    return tour
    
def cheapest_insertion(matrix):
    tours = []
    matrix = __calculate_weighted_matrix(matrix)
    for i in range(len(matrix)):
        tours.append(__nearest_insertion_fixed_start(matrix, i))
    cheapest_route = min(tours, key=lambda k: calc_route_length(k, matrix))
    cheapest_route_costs = calc_route_length(cheapest_route, matrix)
    return cheapest_route, cheapest_route_costs

def __calculate_weighted_matrix(matrix):
    """modifies the already calculated distance matrix and returns a weighted distance matrix"""
    n = len(matrix)
    weighted_matrix = create_matrix(n, n)
    for line in range(n):
        for col in range(n):
            if col%2 == 0:
                weighted_matrix[line][col] = matrix[line][col] * 3
            else:
                weighted_matrix[line][col] = matrix[line][col]
    return weighted_matrix
