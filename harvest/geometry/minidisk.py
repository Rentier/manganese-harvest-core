from __future__ import division

import numpy as np
import random

np.seterr(all='raise') 

class UndefinedCircle():
    def __contains__(self, item): return False   

def minidisk(points, Circle):
    
    def empty(P):
        """ Checks whether a given set P is emtpy """
        return len(P) == 0
    
    def b_md(P, R):
        """ Let b_md(P, R) be the closed disk of smallest radius which
        contains all points in P with all points in R on its boundary.
        """
        if empty(R): 
            return UndefinedCircle()
        elif len(R) == 1: 
            [p] = R            
            return Circle(p1=p, r=0)
        elif len(R) == 2:
            [p, q] = R
            return Circle(p1=p, p2=q)
        elif len(R) == 3:
            [p, q, r] = R
            return Circle(p1=p, p2=q, p3=r)
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
