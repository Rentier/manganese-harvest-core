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

def calc_battle_plan(robots):
	while True:
		points = [ (x,y) for x,y in robots ]
		circle = minidisk(frozenset(points), TaxicabCircle)
		MISSION_TIME = int( np.ceil(circle.r) ) + 1
		GOAL =  np.rint(circle.center()).astype(int)

		if all_can_reach_goal(robots, GOAL, MISSION_TIME):
			return GOAL, MISSION_TIME

def all_can_reach_goal(robots, goal, t):
	for robot in robots:
		if taxicab_distance(robot, goal) > t:
			return False
	return True

def goal_was_reached(data, goal):
	for robot in data[-1]:
		if not np.array_equal(robot, GOAL):
			return False
	return True

if __name__ == '__main__':
	AGENT = "heuristic"
	from_file = False
	write_file = False
	if from_file:
		ROBO_COUNT, robots = io.positions_from_file('tests/robots_100.txt')
	else:
		ROBO_COUNT = 100
		robots = place_robots(ROBO_COUNT)

	if write_file:
		io.positions_to_file("tests/robots_{}.txt".format(ROBO_COUNT), robots)

	assert distance_constraint_holds(robots)

	GOAL, MISSION_TIME = calc_battle_plan(robots)
	assert all_can_reach_goal(robots, GOAL, MISSION_TIME)

	#MISSION_TIME *= 2

	STEPS = MISSION_TIME + 1	
	GOAL_X, GOAL_Y = GOAL

	
	data = np.zeros([STEPS, ROBO_COUNT, 2], dtype=np.int32)
	data[0] = robots

	traveled, collected = fhl.harvest(data, AGENT, GOAL_X, GOAL_Y, STEPS, ROBO_COUNT)
	#assert goal_was_reached(data, GOAL)

	print "Robots: ", ROBO_COUNT
	print "Mission time: ", MISSION_TIME 
	print "Goal: ", GOAL
	print "Traveled: ", traveled
	print "Collected: ", collected
	print "% harvested: ", collected / float(MISSION_TIME * ROBO_COUNT)

	#plot(data,GOAL,interval=100)
	FILENAME = "test_{}_{}.".format(ROBO_COUNT, AGENT)
	#svg(data, FILENAME + "svg")
	png(data, FILENAME + "png")