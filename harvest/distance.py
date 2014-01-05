"""
    Central point for collecting the different
    distance metrics.
"""

import numpy as np

def taxicab_distance(u, v):
    return abs(u[0] - v[0]) + abs(u[1] - v[1])

def euclidean_distance(u, v):
    return np.sqrt( (u[0] - v[0])  ** 2 + (u[1] - v[1]) ** 2 )