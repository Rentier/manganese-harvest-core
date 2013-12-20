import numpy as np

from harvest.geometry.circle import Circle
from harvest.distance import euclidean_distance

#
# Untested after change
#

class EuclideanbCircle(Circle):
    
    def __contains__(self, p):
		return euclidean_distance(self.center(), p) <= self.r
    
    def _from_two_points(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        
        if x1 == x2 or y1 == y2:
            pass# raise Exception("slope == 0 or slope == oo")
    
        c_x = (x1 + x2) / 2
        c_y = (y1 + y2) / 2
        r = euclidean_distance(p1, p2)
        return c_x, c_y, r
    
    def _from_three_points(self, p1, p2, p3):
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

        return c_x, c_y, c_r
