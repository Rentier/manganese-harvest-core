import numpy as np

def constant_from_file(path):
    """
    The data format used  consists of a single
    line, which contains an integer C with
    0 < C <= 100.

    An example for a valid input file:

    42
    """
    
    with open(path, 'r') as f:
        return int(f.readline())

def positions_from_file(path):
    """
    The expected file format is structured the
    following: The first line describes the
    number c of robots. After that, the next c
    lines are coordinates for the robots in the
    format  x y . Valid values for x and y are
    non-negative integers.

    An example for a valid input file:

    3
    0 0
    1 1
    2 1

    """
    with open(path, 'r') as f:
        n = int(f.readline())
        data = np.empty([n, 2], dtype=int)
        
        for i, line in enumerate(f):
            p = [int(i) for i in line.split()]
            assert len(p) == 2
            data[i,0], data[i,1] = p

    return data

def positions_to_file(path, data):
    """
    Same file format as 'Read positions'.
    """
    n = len(data)
    with open(path, 'w') as f:
        f.write("{}\n".format(n))
        for x, y in data:
            f.write("{} {}\n".format(x, y))
        
def mission_to_file(path):
    pass