import sys
import itertools

from harvest.harvester import Harvester

from harvest.agents import *
from harvest.environments import *
from harvest.visualize import *

from harvest.place_robots import place_robots

from harvest.geometry.minidisk import minidisk
from harvest.geometry.taxicab_circle import TaxicabCircle

from harvest.io import *

from harvest.constants import *

def distance_constraint_holds(robots):
    invalid = all(field.distance(r1, r2) > MAX_DISTANCE
                  for (r1,r2) in itertools.combinations(field.robots,2))
    return not invalid

if __name__ == '__main__':
    ROBOT_CNT = 10
    robots = place_robots(ROBOT_CNT)
    #robots = positions_from_file('svg_test.txt')
    field = SquareGrid(robots)
    
    if not distance_constraint_holds(field):
        positions_to_file('invalid_positions.txt', robots)
        print('invalid positions')
        sys.exit(1)

    points = [ (x,y) for x,y in robots ]
    circle = minidisk(frozenset(points), TaxicabCircle)
    mission_time = int( np.ceil(circle.r) )
    #mission_time *= 2

    goal = circle.center()
    agent = LogicalAgent(goal)
    #agent = RandomAgent(goal)
    #visualizer = PlotVisualizer(goal, ROBOT_CNT, mission_time)
    visualizer = SvgVisualizer(goal, ROBOT_CNT, mission_time)
    harvester = Harvester(field, agent, mission_time, visualizer)
    harvester.play()
    print "Mission Time: ", mission_time
    print "Score: ", len(field.collected)
    print "% harvested: ", len(field.collected) / float(mission_time * ROBOT_CNT)
    visualizer.visualize()