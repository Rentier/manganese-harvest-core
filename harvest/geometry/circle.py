from harvest.util import abstract

class Circle():
    
    def __init__(self, p1=None, p2=None, p3=None, r=None):
        if p1 is not None and r is not None:
            self.r = r
            [self.x, self.y] = p1
        elif p1 is not None and p2 is not None and p3 is not None:
            self.x, self.y, self.r = self._from_three_points(p1, p2, p3)
        elif p1 is not None and p2 is not None:
            self.x, self.y, self.r = self._from_two_points(p1, p2)
        else:
            raise Exception('Either one point + radius, two, or three points')
            
    def _from_two_points(self, p1, p2):
        abstract()
        
    def _from_three_points(self, p1, p2, p3):
        abstract()
        
    def __contains__(self, p):
		abstract()
        
    def center(self):
        return (self.x,self.y)
    
    def radius(self):
        return self.r
