class GurobiNotInstalledError(Exception):
    pass

def solve_optimal(matrix):
    """
    Solves a gives tsp instance optimal using the python gurobi solver interface.
    
    Returns a list of indices. The result list has a cardinality
    of the length of the matrix. Raises a GurobiNotInstalled if it cannot import gurobipy
    """
    try:
        import gurobipy as grb
    except:
        raise GurobiNotInstalledError()