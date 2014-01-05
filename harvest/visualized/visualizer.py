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
        self.t = t + 1

        # First dimension is time
        # Second dimension is robots
        # Third dimension is x and y
        # self.data[1][1] asks for the position of the second robot for t=1
        self.positions_x = np.empty([self.t,n], dtype=int)
        self.positions_y = np.empty([self.t,n], dtype=int)

        self.collected = np.empty(self.t, dtype=np.ndarray)

    def on_update(self, field, t):
        self.positions_x[t], self.positions_y[t] = field.robots.copy().T
        self.collected[t] = np.asarray(field.collected.keys())

    def visualize(self, **kwargs):
        abstract()

