import random
from lib import write_matrix_to_csv, calculate_distance_matrix

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
    
def main():
    points = generate_points(10, 0, 10)
    
    matrix=calculate_distance_matrix(points)

    write_matrix_to_csv(matrix,"matrix.csv")
main()