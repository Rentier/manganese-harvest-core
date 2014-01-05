import numpy as np
import itertools

import fharvest.logic as fhl

from harvest.place_robots import place_robots
from harvest.geometry.taxicab_circle import TaxicabCircle
from harvest.geometry.minidisk import minidisk

from harvest.visualize import *

import harvest.io as io

from harvest.distance import *
from harvest.constants import MAX_DISTANCE

def distance_constraint_holds(robots):
	N = len(robots)
	distances = np.empty([N,N])
	for x in xrange(N):
		for y in xrange(N):
			if x != y:
				distances[x,y] = euclidean_distance(robots[x], robots[y])
			else:
				distances[x,y] = -1

	for n in xrange(N):
		valid = any(0 <= x <= MAX_DISTANCE for x in distances[n]  )
		if not valid:
			print n
			print distances[n]
			return False

	return True

def can_reach_goal(robots, goal, t):
	for robot in robots:
		if taxicab_distance(robot, goal) > t:
			print robot, taxicab_distance(robot, goal)

	return True

if __name__ == '__main__':
	from_file = True
	if from_file:
		ROBO_COUNT, robots = io.positions_from_file('tests/robots_100.txt')
	else:
		ROBO_COUNT = 100
		robots = place_robots(ROBO_COUNT)

	assert distance_constraint_holds(robots)

		
	points = [ (x,y) for x,y in robots ]
	circle = minidisk(frozenset(points), TaxicabCircle)

	MISSION_TIME = int( np.ceil(circle.r) )
	STEPS = MISSION_TIME + 2
	GOAL =  np.rint(circle.center()).astype(int)
	GOAL_X, GOAL_Y = GOAL

	assert can_reach_goal(robots, GOAL, MISSION_TIME)

	print MISSION_TIME
	print GOAL
	
	data = np.zeros([STEPS, ROBO_COUNT, 2], dtype=int)
	data[0] = robots

	fhl.harvest(data, GOAL_X, GOAL_Y, STEPS, ROBO_COUNT)
	print "Finished calc"


	plot(data,GOAL)