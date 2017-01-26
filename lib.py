import random
import json
import subprocess
import csv

SETTINGS_FILE = 'settings.ini'

def print_matrix(matrix):
    for line in matrix:
        print(', '.join('{:5.2f}'.format(item) for item in line))
        
def write_matrix_to_csv(matrix, filename):
    with open(filename, 'w') as csvfile:
        for line in matrix:
            line_str = ', '.join(map('{:.5f}'.format, line))
            csvfile.write(line_str + '\n')
            
def read_matrix_from_csv(filename):
    matrix = []
    with open(filename) as csvfile:
        for line in csvfile:
            line = list(map(float, line.strip().split(', ')))
            matrix.append(line)
    return matrix
        
def calculate_distance_matrix(points):
    """returns a distance matrix (euclidean distance).
    points: a list of x,y tuples"""
    n = len(points)
    matrix = create_matrix(n, n)
    for i in range(n):
        for j in range(n):
            # calculate distance between point n and m
            point_1 = points[i]
            point_2 = points[j]
            #matrix[i][j] = round(((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**(1/2), 2)
            matrix[i][j] = round(((point_1[0] - point_2[0])**2 + (point_1[1] - point_2[1])**2)**(1/2), 2)
    return matrix
    
def create_matrix(rows, cols):
    return [[None for j in range(cols)] for i in range(rows)]
    
def calc_route_length(route, matrix):
    route = route[:] + [route[0]]
    length = 0
    for act in range(1, len(route)):
        prev = act - 1
        length += matrix[route[prev]][route[act]]
    return length
    
def print_route(route, matrix):
    route_incl = route[:] + [route[0]]
    route_str = ' -> '.join(map(str, route_incl))
    dist = calc_route_length(route, matrix)
    print('{} [dist: {:.2f}]'.format(route_str, dist))

def generate_points(number, min, max):
    """generates `number` random points in a x,y field - limited by `min` and max"""
    l = []
    for i in range(number):
        x = random.random()
        y = random.random()
        x = round((max-min) * x + min, 2)
        y = round((max - min) * y + min, 2)
        l.append((x,y))
    return l
    
def run_matlab_script(script_name):
    """ Runs a matlab script, waits for its end and returns its output as string encoded"""
    cmd = Settings.get('matlab-executable').replace('%script_name.m%', script_name)
    outp = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    outp = outp.decode('utf-8')
    return outp
    
def create_tsplib_file(filename, point_list):
    with open(filename, 'wt') as file:
        file.write('NAME : {}\n'.format(filename))
        file.write('TYPE : TSP\n')
        file.write('DIMENSION : {}\n'.format(len(point_list)))
        file.write('EDGE_WEIGHT_TYPE : EUC_2D\n')
        file.write('NODE_COORD_SECTION\n')
        for i, point in enumerate(point_list):
            file.write('{} {:.4f} {:.4f}\n'.format(i+1, point[0], point[1]))
        file.write('EOF\n')
    
class Settings:
    __singleton = None
    
    def __init__(self):
        assert Settings.__singleton == None
        # load conf file
        try:
            self.read_settings_file()
        except:
            raise RuntimeError('Reading settings file failed')
            
    def read_settings_file(self):
        self.data = {}
        with open(SETTINGS_FILE) as f:
            for line in f:
                line = line.strip()
                if line == '' or line.startswith('#'):
                    continue
                key, value = line.split('=')
                self.data[key] = value
            
    @staticmethod
    def __get_singleton():
        if Settings.__singleton == None:
            Settings.__singleton = Settings()
        return Settings.__singleton
        
    @staticmethod
    def get(key):
        return Settings.__get_singleton().data.get(key)
    
    
    
    
