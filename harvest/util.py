from harvest.distance import *

def abstract():
    """Indicates that a method is abstract
    and needs to be implemented by a subclass
    """
    raise NotImplementedException('Subclass needs to implement')

def nearest_neighbour(points, p, distance=euclidean_distance):
	""" Returns the nearest number of p in from a  set of points
	"""
	index = np.argmin([distance(p,x) for x in points])
	return points[index]

