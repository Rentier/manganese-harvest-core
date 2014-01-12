import numpy as np

class Field():
	
	def __init__(self, robots):
		"""
			robots: 
				Sequence of robots. A robot here is a 
				simple np.array(dtype=np.array([x,y]) and
				identified by its index to the robots array
		"""
		self.robots = robots
		self.mangan_statistics = np.zeros(len(robots), dtype=np.int)
	
	def neighbours(self, p):
		abstract()    
	
	def move_robot(self, robot, dx, dy):
		abstract()
	
	def has_robot(self, p):
		abstract()
		
	def distance(self, p, q):
		""" Returns the number of steps required to reach q from p"""
		abstract()
		

	def is_harvested(self, p):
		""" Returns True when the tile at position p is harvested,
		i.e. empty, or False, when it is untouchd.
		"""
		abstract()
