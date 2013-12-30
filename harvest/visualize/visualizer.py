import numpy as np

from harvest.util import abstract

class Visualizer():

    def __init__(self, goal, n, t):
        """
            goal: Destination point of the robots
            n: number of robots
            t: maximum mission time
        """
        self.goal = goal
        self.n = n
        self.t = t

        # First dimension is time
        # Second dimension is robots
        # Third dimension is x and y
        # self.data[1][1] asks for the position of the second robot for t=1
        self.positions = np.empty([t,n,2], dtype=int)

        self.collected = np.empty(t, dtype=np.ndarray)

    def on_update(self, field, t):
        self.positions[t] = field.robots.copy()
        self.collected[t] = np.asarray(field.collected.keys())

    def visualize(self):
        abstract()

