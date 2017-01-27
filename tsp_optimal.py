import os.path
import subprocess
import numpy as np
from tempfile import TemporaryDirectory

# try to import gurobi
try:
    from gurobipy import Model, quicksum, GRB
except: pass
# try to import pulp
try:
    import pulp
except: pass
# try to import lpsolve55
try:
    from lpsolve55 import lpsolve, GE, LE, EQ, IMPORTANT
except: pass

from lib import create_tsplib_file, Settings

    
def solve_optimal(matrix, point_list):
    if Settings.get('optimal_solver') == 'gurobi':
        return solve_optimal_gurobi(matrix)
    else:
        # use concorde
        return solve_optimal_concorde(point_list)
        
def solve_optimal_concorde(point_list):
    # create a point list file
    with TemporaryDirectory() as tmpdirname:
        tsp_filename = 'tsp_file.tsp'
        tsp_fullname = os.path.join(tmpdirname, tsp_filename)
        create_tsplib_file(tsp_fullname, point_list)
        conc_exe = Settings.get('concorde_executable')
        if not os.path.isabs(conc_exe):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            conc_exe = os.path.join(dir_path, conc_exe)
        # call concorde in tmp folder
        process = subprocess.Popen([conc_exe, tsp_filename],
            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, cwd=tmpdirname)
        #output = process.stdout.read()
        #output_err = process.stderr.read()
        exit_code = process.wait()
        if exit_code != 0:
            raise RuntimeError('concorde returned an error')
        
        # read output of concorde
        tour = []
        with open(tsp_fullname[:-4] + '.sol') as sol_file:
            sol_file.readline()
            for line in sol_file:
                line = map(int, line.strip().split())
                tour.extend(line)
        if len(tour) != len(point_list):
            raise RuntimeError('concorde returned a wrong tour')
        return tour
        
def solve_optimal_lpsolve(matrix):
    """
    Solves a given tsp instance optimal using the open source lpsolve solver.
    
    Returns a list of indices. The result list has a cardinality
    of the length of the matrix.
    """
    n = len(matrix); N = list(range(n))
    ij = [(i,j) for i in N for j in N]
    obj_factors = [matrix[i][j] for i,j in ij] + [0 for i in N]
    
    lp = lpsolve('make_lp', 0, len(obj_factors))
    ret = lpsolve('set_lp_name', lp, 'tsp_model')
    lpsolve('set_verbose', lp, IMPORTANT)
    lpsolve('set_obj_fn', lp, obj_factors)
    # set var names:
    for num, (i,j) in enumerate(ij):
        lpsolve('set_col_name', lp, num+1, 'x{}{}'.format(i, j))
        lpsolve('set_binary', lp, num+1, 1)
    for num in range(len(ij), len(ij)+len(N)):
        lpsolve('set_col_name', lp, num+1, 'u{}'.format(num-len(ij)))
    # Constraints for assignment problem:
    # sum of all 
    for row in N:
        lpsolve('add_constraint', lp, [1 if i == row else 0 for i,j in ij] + [0 for i in N], EQ, 1)
    for col in N:
        lpsolve('add_constraint', lp, [1 if j == col else 0 for i,j in ij] + [0 for i in N], EQ, 1)
    # first subtour elimation constraints:
    for u in N[1:]:
        lpsolve('add_constraint', lp, [0 for i,j in ij] + [1 if u == i else 0 for i in N], GE, 2)
        lpsolve('add_constraint', lp, [0 for i,j in ij] + [1 if u == i else 0 for i in N], LE, n)
    # second subtour elimination constraints:
    for (i,j) in ((i,j) for i in N[1:] for j in N[1:]):
        # ui - uj + xij (n-1) <= n - 2
        x_factors = [(n-1) if i == i_ and j == j_ else 0 for i_, j_ in ij]
        both = i == j
        u_factors = []
        for u in N:
            if (u == i or u == j) and (i == j):
                u_factors.append(0)
            elif u == i:
                u_factors.append(-1)
            elif u == j:
                u_factors.append(1)
            else:
                u_factors.append(0)
        lpsolve('add_constraint', lp, x_factors + u_factors, LE, n - 2)
    
    #lpsolve('write_lp', lp, 'lpsolve.lp')
    ret = lpsolve('solve', lp)
    if ret != 0:
        if ret == 2:
            print('Solution Infeasible')
            exit()
        else:
            raise RuntimeError('Some lpsolve error')
    vars = lpsolve('get_variables', lp)[0]
    return __lps_retrieve_tour(vars[:len(ij)])
    
def __lps_retrieve_tour(vars):
    n = int(len(vars) ** (1/2))
    # reshape x:
    x = np.reshape(np.array(vars, dtype=int), (n, n))
    return __retrieve_tour_from_array(x)
    
def solve_optimal_coin_pulp(matrix):
    """
    Solves a given tsp instance optimal using the python pulp interface to the coin solver.
    
    Returns a list of indices. The result list has a cardinality
    of the length of the matrix.
    """
    n = len(matrix); N = list(range(len(matrix)))
    prob = pulp.LpProblem('tsp_problem', pulp.LpMinimize)
    # The problem variables are created
    x = pulp.LpVariable.dicts("x",(N, N),0,1, pulp.LpInteger)
    u = pulp.LpVariable.dicts("u",(N),0 ,n)
    print(u)
    print(x)

def solve_optimal_gurobi(matrix):
    """
    Solves a given tsp instance optimal using the python gurobi solver interface.
    
    Returns a list of indices. The result list has a cardinality
    of the length of the matrix. Raises a GurobiNotInstalled if it cannot import gurobipy
    """
    model = Model()
    model.Params.OutputFlag = 0
    n = len(matrix); N = list(range(n))
    # Create variables
    x = [[model.addVar(vtype=GRB.BINARY, ub=1.0, lb=0.0, name='x{}{}'.format(i,j)) for j in N] for i in range(n)]
    u = [ model.addVar(vtype=GRB.CONTINUOUS, name='u{}'.format(i))  for i in N] # miller tucker vars
    model.update()
    # Set objective
    sum_tour_length = [x[i][j] * matrix[i][j] for i in N for j in N]
    model.setObjective(quicksum(sum_tour_length), GRB.MINIMIZE)
    # Constraints for assignment problem:
    [model.addConstr(quicksum([x[i][j] for j in range(n)]) == 1)   for i in N]
    [model.addConstr(quicksum([x[i][j] for i in range(n)]) == 1)   for j in N]
    # Constraints for subtour elimination:
    [model.addConstr(2 <= u[i] <= n) for i in N[1:]]
    [model.addConstr(u[i] - u[j] + 1 <= (n-1)*(1-x[i][j]))   for i in N[1:] for j in N[1:]]
    #model.write('gurobi.lp')
    model.optimize()
    if model.status == GRB.Status.OPTIMAL:
        return __grb_retrieve_tour(model, x)
        
def __retrieve_tour_from_array(array):
    def __find_next_city_in_line(line):
        for i, var in enumerate(line):
            if var == 1:
                return i
    
    last_city = __find_next_city_in_line(array[0])
    tour = [last_city]
    while True:
        next_city = __grb_find_next_city_in_line(array[last_city])
        if next_city == tour[0]:
            break
        else:
            tour.append(next_city)
            last_city = next_city
    return tour
        
    
def __grb_retrieve_tour(model, x):
    """ gurobi helper function """
    # create a numpy array
    array = np.empty((len(x), len(x)), dtype=int)
    for i, line in enumerate(x):
        for j, var in enumerate(line):
            array[i,j] = int(var.X)
    return __retrieve_tour_from_array(array)

def __grb_find_next_city_in_line(line):
    """ gurobi helper function """
    for i, var in enumerate(line):
        if var == 1:
            return i
