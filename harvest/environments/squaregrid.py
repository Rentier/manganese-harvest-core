import random
import numpy as np

from harvest.environments.field import Field
from harvest.util import abstract

from harvest.distance import taxicab_distance

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
        assert self.distance(robot,p) <= 1
        robot[0], robot[1] = p
        
    def has_robot(self, p):
        return p in self.robots
    
    def distance(self, p, q):
        return taxicab_distance(p, q)
    
    def is_harvested(self, ):
        return self.collected.get(tuple(p), False)
