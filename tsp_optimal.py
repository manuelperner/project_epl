class GurobiNotInstalledError(Exception):
    pass

def solve_optimal(matrix):
    """
    Solves a given tsp instance optimal using the python gurobi solver interface.
    
    Returns a list of indices. The result list has a cardinality
    of the length of the matrix. Raises a GurobiNotInstalled if it cannot import gurobipy
    """
    #__check_gurobi
    from gurobipy import Model, quicksum, GRB
    model = Model()
    model.Params.OutputFlag = 0
    n = len(matrix); N = list(range(n))
    # Create variables
    x = [[model.addVar(vtype=GRB.BINARY, ub=1.0, lb=0.0) for j in N] for i in range(n)]
    u = [ model.addVar(vtype=GRB.CONTINUOUS)  for i in N] # miller tucker vars
    # Set objective
    sum_tour_length = [x[i][j] * matrix[i][j] for i in N for j in N]
    model.setObjective(quicksum(sum_tour_length), GRB.MINIMIZE)
    # Constraints for assignment problem:
    [model.addConstr(quicksum([x[i][j] for j in range(n)]) == 1)   for i in N]
    [model.addConstr(quicksum([x[i][j] for i in range(n)]) == 1)   for j in N]
    # Constraints for subtour elimination:
    [model.addConstr(2 <= u[i] <= n) for i in N[1:]]
    [model.addConstr(u[i] - u[j] + 1 <= (n-1)*(1-x[i][j]))   for i in N[1:] for j in N[1:]]
    pass
    model.optimize()
    if model.status == GRB.Status.OPTIMAL:
        return __rerieve_tour(model, x)
        
def __check_gurobi():
    try:
        import gurobipy
    except:
        raise GurobiNotInstalledError()
        
    
def __rerieve_tour(model, x):
    N = list(range(len(x)))
    last_city = __find_next_city_in_line(x[0])
    tour = [last_city]
    while True:
        next_city = __find_next_city_in_line(x[last_city])
        if next_city == tour[0]:
            break
        else:
            tour.append(next_city)
            last_city = next_city
    return tour

def __find_next_city_in_line(line):
    for i, var in enumerate(line):
        if int(var.X) == 1:
            return i