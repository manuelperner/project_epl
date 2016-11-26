"""
This module offers some tsp heuristics

Each heuristic is implemented in a seperate python file and they
are all shared by this module

It would also be possible to implement some heuristics in a different
programming language. This module would be the perfect place to
put together all different solutions and offering it to a user interface
"""

from tsp_heuristics.nearest_neighbour import tsp_nearest_neighbour as nearest_neighbour