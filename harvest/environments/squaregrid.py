import random
import numpy as np

from harvest.environments.field import Field
from harvest.util import abstract

class SquareGrid(Field):
    """ Assumes that the world is divided in an infinite squared 
    2D-grid with a grid width of 1 meter    
    """

    def __init__(self, robots):
        Field.__init__(self, robots)
        # Change this datastructure to something more reasonable
        self.collected = {}
        
    def neighbours(self, p):
        return np.array([[p[0]-1,p[1]],[p[0]+1,p[1]],[p[0],p[1]-1],[p[0],p[1]+1]])
    
    def move_robot(self, robot, p):
        
        # assert distance <= 1
        print(robot)
        robot[0], robot[1] = p
        print(robot)
        
    def has_robot(self, p):
        return p in self.robots
    
    def distance(self, p, q):
        return np.abs(p[0] - q[0]) + np.abs(p[1] - q[1])
    
    def is_harvested(self, ):
        return self.collected.get(tuple(p), False)
