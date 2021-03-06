import random
import json
import subprocess
import csv
import os.path

SETTINGS_FILE = 'settings.ini'
SETTINGS_DEFAULT = 'settings_default.ini'

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

def generate_points(number, min_val, max_val):
    """generates `number` random points in a x,y field - limited by `min` and max"""
    l = []
    for i in range(number):
        x = random.random()
        y = random.random()
        x = round((max_val-min_val) * x + min_val, 2)
        y = round((max_val - min_val) * y + min_val, 2)
        l.append((x,y))
    return l
    
def run_matlab_script(script_name):
    """ Runs a matlab script, waits for its end and returns its output as string encoded"""
    cmd = Settings.get('matlab-executable').replace('%script_name.m%', script_name)
    outp = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    outp = outp.decode('utf-8')
    return outp
    
def create_tsplib_file(filename, point_list):
    max_val = max(max(point[0], point[1]) for point in point_list)
    factor = 10000/max_val
    with open(filename, 'wt') as file:
        file.write('NAME : {}\n'.format(filename))
        file.write('TYPE : TSP\n')
        file.write('DIMENSION : {}\n'.format(len(point_list)))
        file.write('EDGE_WEIGHT_TYPE : EUC_2D\n')
        file.write('NODE_COORD_SECTION\n')
        for i, point in enumerate(point_list):
            file.write('{} {} {}\n'.format(i+1, int(point[0]*factor), int(point[1]*factor)))
        file.write('EOF\n')
    
class Settings:
    __singleton = None
    
    def __init__(self):
        # load conf file
        try:
            self.read_settings_file()
        except:
            raise RuntimeError('Reading settings file failed')
            
    def read_settings_file(self):
        settings_file = SETTINGS_FILE
        if not os.path.isfile(settings_file):
            settings_file = SETTINGS_DEFAULT
        self.data = {}
        with open(settings_file) as f:
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
    
    
    
    
