import numpy as np
import scipy.spatial
import matplotlib.pyplot as plt

##
# Constants
##

N = 100 # Number of robots
MAX_DISTANCE = 200
FRAMES = 30

##
# Helper functions
##

def distance(u,v):
    return scipy.spatial.distance.euclidean(u,v)

def nearest_neighbour(points, p):
    """ Returns the nearest number of p in
    a set of points
    """
    index = np.argmin([distance(p,x) for x in points])
    return points[index]

def smallest_enclosing_circle(points):
    """ Solution of the Minimal Enclosing Circle problem.
    Calculates radius and centre of the circle which
    contains all points on its borders or its area
    with the minimal radius.
    """
    
    pass 
    

###
# Generate stuff
##

def generate_point(x_min, y_min, x_max, y_max):
    x = np.random.random_integers(x_min,x_max,1)
    y = np.random.random_integers(y_min,y_max,1)
    return np.array([x,y], int)

def generate_point_boxed(min_x, min_y, max_x, max_y):
    """ Generates a point which coordinates lie
    in a box which borders are determined by the
    min and max values given, plus a margin of
    MAX_DISTANCE size around it.
    """
    x_min = max(0, min_x - MAX_DISTANCE)
    y_min = max(0, min_y - MAX_DISTANCE)
    x_max = max_x + MAX_DISTANCE
    y_max = max_y + MAX_DISTANCE
    return generate_point(x_min, y_min, x_max, y_max)

def generate_first_robot():
    return generate_point(0,0,10000,10000)

def generate_data():
    data = np.zeros((N,2), int)
    data[0,0], data[0,1] = generate_first_robot()
    
    # Keeps the coordinates of the box
    # in which potential points may lie
    min_x, min_y = np.amin(data, axis=0)
    max_x, max_y = np.amax(data, axis=0)
    
    for i in range(1, N):               
        while True:
            p = generate_point_boxed(min_x, min_y, max_x, max_y)
            nearest = nearest_neighbour(data[:i], p)
            if distance(p, nearest) <= MAX_DISTANCE:
                break
        
        data[i,0], data[i,1] = p
        
        min_x, min_y = np.amin(data, axis=0)
        max_x, max_y = np.amax(data, axis=0)
    
    return data

def normalize_data(points):
    min_x, min_y = np.amin(points, axis=0)
    normalized = np.zeros_like(points)
    for i, (p_x, p_y) in enumerate(points):
        normalized[i][0] = p_x - min_x
        normalized[i][1] = p_y - min_y
    return normalized

##
# Graphics
##

def plot(data):    
    max_x, max_y = np.amax(data, axis=0)
    
    LIM = max(max_x, max_y) * 1.1
    
    fig, axes = plt.subplots(figsize=(12,12))
    axes.set_ylim([0, LIM])
    axes.set_xlim([0, LIM])
    
    # Draw distance circles
    for p in data:
        circle = plt.Circle(p,MAX_DISTANCE,color='g')
        fig.gca().add_artist(circle)
    
    plt.plot(*np.transpose(data), marker='o', color='r', ls='')
    plt.show()
    
if __name__ == "__main__":         
    points = generate_data()
    normalized_data = normalize_data(points)
    plot(normalized_data)
