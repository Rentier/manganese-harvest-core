import random

from harvest.agents.agent import Agent
from harvest.distance import euclidean_distance
from harvest.constants import MAX_DISTANCE

class RandomAgent(Agent):

    def __init__(self, goal):
        self.goal = goal

    def is_legal_transition(self, robot, p, field, t):
        """ Returns whether the transition from the current
        position of the robot to point p is a valid one. I. e. :

        The robot stays in range of at least one other robot
        The robot can reach the goal point
        """
        return field.is_reachable(robot, p, t) and \
            euclidean_distance(robot, p) <= MAX_DISTANCE
    
    def calc(self, robot, field, t):
        """ Chooses randomly between legal movement choices """
        moves = [neighbour for neighbour in field.neighbours(robot) 
                 if field.distance(self.goal, neighbour) <= t]
        if moves: field.move_robot(robot, random.choice(moves))
