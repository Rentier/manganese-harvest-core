import numpy as np

from harvest.geometry.circle import Circle
from harvest.distance import taxicab_distance

rotation_matrix_45 = np.array([[np.cos(-np.pi/4), - np.sin(-np.pi/4)],
                               [np.sin(-np.pi/4),   np.cos(-np.pi/4)]])

rotation_matrix_minus_45 = rotation_matrix_45.T

def rotate_by_45(p):
    return rotation_matrix_45.dot(p)

def unrotate_by_45(p):
    return rotation_matrix_minus_45.dot(p)

# unrotate_by_45( rotate_by_45(p) ) == p

class TaxicabCircle(Circle):
    
    def __contains__(self, p):
		return taxicab_distance(self.center(), p) <= self.r
    
    def _from_two_points(self, p1, p2):
        x1,y1 = p1
        x2,y2 = p2
        c_x = (x2 + x1) / 2
        c_y = (y2 + y1) / 2
        c = (c_x, c_y)
        d1 = taxicab_distance(p1, c)
        d2 = taxicab_distance(p2, c)
        r = max(d1, d2)
        return c_x, c_y, r
    
    def _from_three_points(self, p1, p2, p3):
        x1r, y1r = rotate_by_45(p1)
        x2r, y2r = rotate_by_45(p2)
        x3r, y3r = rotate_by_45(p3)
        
        s = max(np.abs(x1r-x2r), np.abs(x1r-x3r), np.abs(x2r-x3r),
                np.abs(y1r-y2r), np.abs(y1r-y3r), np.abs(y2r-y3r))
        
        # Lower left point
        ll_x = min(x1r, x2r, x3r)
        ll_y = min(y1r, y2r, y3r)
        
        # Center point  
        c_xr = ll_x + s / 2
        c_yr = ll_y + s / 2
        
        r = np.sqrt( (ll_x - c_xr) ** 2 + (ll_y - c_yr) ** 2 )
        
        c_x, c_y = unrotate_by_45(np.array([c_xr, c_yr]))

        return c_x, c_y, r
        
