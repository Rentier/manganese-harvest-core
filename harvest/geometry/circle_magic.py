from __future__ import division

import numpy as np
import operator
import random

np.seterr(all='raise') 

class CircleComputeException(Exception):
    pass
    
class UndefiendCircle():
    def __contains__(self, item): return False 

class Circle:
    
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        
    def center(self):
        return (self.x, self.y)
    
    def radius(self):
        return self.radius
    
    @staticmethod
    def singularity(p):
        x, y = p
        return Circle(x,y,0)
    
    @staticmethod
    def from_two_points(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2 or y1 == y2:
            pass# raise Exception("slope == 0 or slope == oo")
    
        c_x = (x1 + x2) / 2
        c_y = (y1 + y2) / 2
        r = scipy.spatial.distance.euclidean(p1,p2) / 2
        return Circle(c_x, c_y, r)

    @staticmethod
    def from_three_points(p1, p2, p3):
        """ http://www.ehow.com/how_5899905_radius-three-points.html   """  
        x1,y1 = p1
        x2,y2 = p2
        x3,y3 = p3
        
        x1,y1 = float(x1), float(y1)
        x2,y2 = float(x2), float(y2)
        x3,y3 = float(x3), float(y3)
        
        def central_point(p1, p2, p3, dim):
            foo = max(p1, p2, key=operator.itemgetter(dim))
            return min(p3, foo, key=operator.itemgetter(dim))
        
        # If the points are collinear, instead return a circle
        # which simply contains the central point and has the 
        # others on its border
        
        if x1 == x2 == x3:
            top = max(p1, p2, p3, key=operator.itemgetter(1))
            bottom = min(p1, p2, p3, key=operator.itemgetter(1))
            return circle_from_two_points(top,bottom)
            
        if y1 == y2 == y3:
            left = max(p1, p2, p3, key=operator.itemgetter(0))
            right = min(p1, p2, p3, key=operator.itemgetter(0))
            return circle_from_two_points(left,right)
    
        x1s, y1s = x1 ** 2, y1 ** 2
        x2s, y2s = x2 ** 2, y2 ** 2
        x3s, y3s = x3 ** 2, y3 ** 2
        
        c_x = ((y1-y2) * (x3s+y3s) + (y2-y3) * (x1s + y1s) + (y3 - y1) * (x2s + y2s )) / \
              (2 * ((y1-y2)*x3  + (y3-y1)*x2 + (y2-y3)*x1))
        c_y = ((x1-x2) * (x3s+y3s) + (x2-x3) * (x1s + y1s) + (x3 - x1) * (x2s + y2s )) / \
              (2 * ((x1-x2)*y3  + (x3-x1)*y2 + (x2-x3)*y1))
        c_r = np.sqrt((c_x - x1)**2 + (c_y - y1)**2)
        
        return  Circle(c_x,c_y,c_r)
    
    def __contains__(self, p):
        return (p[0] - self.x)  ** 2 + (p[1] - self.y) ** 2 <= self.r ** 2
    
    def __str__(self):
        return "Center: ({}, {}), r: {}".format(self.x,self.y,self.r)    

def minidisk(points):
    
    def empty(P):
        """ Checks whether a given set P is emtpy """
        return len(P) == 0
    
    def b_md(P, R):
        """ Let b_md(P, R) be the closed disk of smallest radius which
        contains all points in P with all points in R on its boundary.
        """
        if empty(R): 
            return UndefiendCircle()
        elif len(R) == 1: 
            [[x,y]] = R            
            return Circle(x, y, 0)
        elif len(R) == 2:
            [p1, p2] = R
            return Circle.from_two_points(p1, p2)
        elif len(R) == 3:
            [p1, p2, p3] = R
            return Circle.from_three_points(p1, p2, p3)
        else:
            raise Exception("Should not happen!")        

    def b_minidisk(P,R):
        """ Computes the smallest disk enclosing points P
        with points R on its boundary
        """
        if empty(P) or len(R) == 3:
            D = b_md(frozenset(), R)
        else:
            p = random.sample(P, 1)[0] # Take random element out of P
            p_as_set = frozenset((p,))
            D = b_minidisk(P - p_as_set, R)
            if p not in D:
                D = b_minidisk(P - p_as_set, R | p_as_set)                
        return D
        
    return b_minidisk(points, frozenset() )
