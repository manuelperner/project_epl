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
    
def first_come_first_serve(matrix):
    return list(range(len(matrix)))
     
def nearest_insertion(matrix):
    raise NotImplementedError()
    
def cheapest_insertion(matrix):
    raise NotImplementedError()
    
def mst_heuristic(matrix):
    mst_graph = _kruskal(matrix)
    assert len(mst_graph) == len(matrix) - 1
    graph = []
    for edge in mst_graph:
        reversed_edge = {'from' : edge['to'], 'to': edge['from'], 'dist' : edge['dist']}
        graph.append(edge)
        graph.append(reversed_edge)
    # create tour
    first_edge = graph[0]
    tour = [first_edge['from'], first_edge['to']]
    print(tour)
    
def _kruskal(matrix):
    """ Returns a list of edges that spans a minimum spaning tree """
    n = len(matrix)
    # create edges
    edges = list()
    for i in range(n-1):
        for j in range(i+1, n):
            edge = {'from' : i, 'to': j, 'dist' : matrix[i][j]}
            edges.append(edge)
    # create a cycle free graph:
    graph = []
    while len(edges) > 0:
        # find the shortest edge in list:
        shortest_edge = min(edges, key= lambda k: k['dist'])
        new_graph = graph + [shortest_edge]
        if not _is_cycle(new_graph):
            graph = new_graph
        edges.remove(shortest_edge)
    return graph
    
def test_is_cycle():
    g = [{'from': 3, 'to': 5, 'dist': 0.86},    
        {'from': 2, 'to': 4, 'dist': 1.82},
{'from': 0, 'to': 6, 'dist': 2.01},
{'from': 1, 'to': 6, 'dist': 2.67},
{'from': 0, 'to': 1, 'dist': 3.33},
{'from': 0, 'to': 4, 'dist': 5.31},
{'from': 1, 'to': 4, 'dist': 6.49},
{'from': 0, 'to': 2, 'dist': 7.03},
{'from': 4, 'to': 6, 'dist': 7.09},
{'from': 1, 'to': 2, 'dist': 7.73},
{'from': 2, 'to': 6, 'dist': 8.71}]
    cycle = _is_cycle(g)
    
 
def _is_cycle(graph):
    all_vertices = set()
    for edge in graph:
        all_vertices.add(edge['from'])
        all_vertices.add(edge['to'])
    for i in all_vertices:
        if _is_cycle_start_point(graph, i):
            return True
    return False

        
def _is_cycle_start_point(graph, start_point):
    """ Checks if a given list of edges has a cycle - returns True if a cycle exists"""
    visited = []
    def explore(node_nr, parent_nr):
        #print('Node_nr: {}, parent_nr: {}'.format(node_nr, parent_nr))
        if node_nr in visited:
            return True
        else:
            visited.append(node_nr)
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

def check_cycles(adj_m):
    """Checks whether a given adjacency matrix has cycles in it"""
    visited = []
    
    def explore(node, parent):
        if node in visited:
            return True
        else:
            visited.append(node)
            neighbours = getNeighboursOfVertex(adj_m, node)
            neighbours = list(filter(lambda a: a != parent, neighbours))
            for u in neighbours:
                if explore(u, node):
                    return True
            return False
    return explore(0,None)
    
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