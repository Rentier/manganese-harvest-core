import random
from collections import defaultdict

from harvest.agents.agent import Agent

class LogicalAgent(Agent):
    
    def __init__(self, goal):
        self.goal = goal
        
    def choose_unharvested_move(self, field, moves):
        new_moves = [neighbour for neighbour in moves 
                     if field.is_harvested(neighbour) == False]
        return new_moves
    
    def choose_max_distance_to_robots_moves(self, robot, field, moves):
        closest_robots_dict = defaultdict(list)
        for r in field.robots:
            distance = field.distance(r, robot)
            if distance == 0:
                continue
            closest_robots_dict[distance].append(r)
            
        # first idea was to limit the size of the dictionary.. turns out to be not too easy..
        # broken code below
        '''
        CLOSEST_CNT = 3
        elements_cnt = 0
        max_distance = None
        closest_robots_dict = defaultdict(list)
        for r in field.robots:
            distance = field.distance(r, robot)
            print distance
            if distance == 0:
                continue
            if elements_cnt < CLOSEST_CNT:
                if max_distance == None or distance > max_distance:
                    max_distance = distance
                closest_robots_dict[distance].append(r)
                elements_cnt += 1
            elif distance < max_distance:
                del closest_robots_dict[max_distance]
                closest_robots_dict[distance].append(r)
                max_distance = max(closest_robots_dict.keys(), key = int)
        '''
            
        sorted_distances = list(sorted(closest_robots_dict.keys()))
        closest_robots = list()
        for key in sorted_distances:
            closest_robots += closest_robots_dict[key]
        
        move_iterator = list(moves)
        max_distance = None
        for cr in closest_robots:
            new_moves = list()
            for m in move_iterator:
                distance = field.distance(cr, m)
                if not new_moves:
                    new_moves.append(m)
                    max_distance = distance
                elif distance > max_distance:
                    new_moves = list()
                    new_moves.append(m)
                    max_distance = distance
                elif distance == max_distance:
                    new_moves.append(m)
            if len(new_moves) == 1:
                break
            move_iterator = list(new_moves)
        
        return new_moves
    
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
            new_moves = self.choose_max_distance_to_robots_moves(robot, field, moves)
            if new_moves:
                moves = list(new_moves)
            field.move_robot(robot, random.choice(moves))
