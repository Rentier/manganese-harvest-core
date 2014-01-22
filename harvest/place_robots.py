import numpy as np
import matplotlib.pyplot as plt
from random import choice

from harvest.distance import euclidean_distance as distance
from harvest.constants import MAX_DISTANCE

def normalize_data(points):
	min_x, min_y = np.amin(points, axis=0)
	normalized = np.zeros_like(points)
	for i, (p_x, p_y) in enumerate(points):
		normalized[i][0] = p_x - min_x
		normalized[i][1] = p_y - min_y
	return normalized

def generate_first_robot(n):
	v = (MAX_DISTANCE + 1) * n
	return np.array([v,v])

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

def nearest_neighbour(points, p):
	""" Returns the nearest number of p in from aset of points
	"""
	index = np.argmin([distance(p,x) for x in points])
	return points[index]

def generate_point(x_min, y_min, x_max, y_max):
	x = np.random.random_integers(x_min,x_max,1)
	y = np.random.random_integers(y_min,y_max,1)
	return np.array([x,y], int)


def place_robots_slow(n):
	""" Slower, but gives a more spread distribution """
	data = np.zeros((n,2), int)
	data[0,0], data[0,1] = generate_first_robot(n)
		
	# Keeps the coordinates of the box
	# in which potential points may lie
	min_x, min_y = np.amin(data, axis=0)
	max_x, max_y = np.amax(data, axis=0)
		
	for i in range(1, n):
		while True:
			p = generate_point_boxed(min_x, min_y, max_x, max_y)
			nearest = nearest_neighbour(data[:i], p)
			if distance(p, nearest) <= MAX_DISTANCE:
				break
			
		data[i,0], data[i,1] = p
			
		min_x, min_y = np.amin(data, axis=0)
		max_x, max_y = np.amax(data, axis=0)
	return data

def place_robots_fast(n):		
	data = np.zeros((n,2), int)
	data[0,0], data[0,1] = generate_first_robot(n)
	for i in range(n):
		pivot = choice(data)
		while True:
			xmin, ymin = pivot[0] - MAX_DISTANCE, pivot[1] - MAX_DISTANCE
			xmax, ymax = pivot[0] + MAX_DISTANCE, pivot[1] + MAX_DISTANCE
			p = generate_point(xmin,ymin,xmax,ymax)
			if distance(p, pivot) <= MAX_DISTANCE:
				break
		data[i,0], data[i,1] = p
	return data

def place_robots(n):	
	data = place_robots_slow(n) if n <= 30 else place_robots_fast(n)
	return normalize_data(data)
