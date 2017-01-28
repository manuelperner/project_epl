import lib
from tsp_heuristics import _kruskal

matrix = lib.read_matrix_from_csv('matrix.csv')
mst_graph = _kruskal(matrix)
for edge in mst_graph:
    print(edge)
