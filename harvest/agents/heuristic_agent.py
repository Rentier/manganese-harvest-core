import random
from collections import defaultdict

import numpy as np
import scipy.spatial as ss

from harvest.agents.agent import Agent

NEAREST_NEIGHBOURS = 5

class HeuristicAgent(Agent):
    
    def __init__(self, goal):
        self.goal = goal
        
    def choose_unharvested_move(self, field, moves):
        new_moves = [neighbour for neighbour in moves if not field.is_harvested(neighbour)]
        return new_moves
    
    def choose_max_distance_to_robots_moves(self, robot, field, moves):
        tree = ss.KDTree(field.robots)
        # p=1 means use taxicab distance
        [distances, indices] = tree.query(moves, NEAREST_NEIGHBOURS, p=1)

        reduced_distances = distances.sum(axis=1)

        max_index = np.argmax(reduced_distances)
        return moves[max_index]
    
    def calc(self, robot, field, t):
        moves = [neighbour for neighbour in field.neighbours(robot) 
                 if field.distance(self.goal, neighbour) <= t]
        if moves:
            ''' 1st: from all possible moves only keep those which increase the score '''
            new_moves = self.choose_unharvested_move(field, moves)
            if new_moves:
                moves = list(new_moves)
            ''' 2st: from the moves left (or all if no unharvested neighbour) choose 
                the move which maximizes the distances to nearest robots (could be 
                more than one move, but unlikely) '''
            best_move = self.choose_max_distance_to_robots_moves(robot, field, moves)
            field.move_robot(robot, best_move)