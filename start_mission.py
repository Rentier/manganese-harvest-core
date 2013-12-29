from harvest.agents import *
from harvest.environments import *

from harvest.harvester import Harvester
from harvest.place_robots import place_robots
from harvest.geometry.minidisk import minidisk
from harvest.geometry.taxicab_circle import TaxicabCircle

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from math import sqrt

class PrintAnimator():

    def __init__(self, goal):
        self.goal = goal
        self.x = []
        self.y = []

    def on_update(self, field):
        tmp_x , tmp_y = np.transpose(field.robots.copy())
        self.x.append(tmp_x)
        self.y.append(tmp_y)

    def movietime(self, vid=False):
        mission_time = len(self.x)
        border = mission_time  + 5 
        xmid, ymid = self.goal
    
        fig  = plt.figure()
        axis = plt.gca() 
        line, = axis.plot([], [], linestyle='none', marker='o', color='r', ms=3., zorder=42)

        axis.set_xlim([xmid-border, xmid+border])    
        axis.set_ylim([ymid-border, ymid+border])
        axis.xaxis.set_visible(False)
        axis.yaxis.set_visible(False)

        t = np.arange(0, mission_time)
        
        # Patch for euclidean circle
        # patch = plt.Circle(self.goal, mission_time, fc='c', animated=True, lw=0, zorder=0, alpha=.1)

        # Patch for taxicab circle
        patch = matplotlib.patches.RegularPolygon(self.goal, 4, radius=mission_time, color='g', animated=True, zorder=0, alpha=.1, lw=0, fc='c')    

        axis.set_aspect('equal')
        
        def init():
            line.set_data([],[])
            patch.center = self.goal
            patch.radius = mission_time
            axis.add_patch(patch)
            return line, patch

        def animate(i):
            line.set_data(self.x[i],self.y[i])
            patch.radius = mission_time - i
            return line, patch
            
        ani = animation.FuncAnimation(fig, animate, t, blit=True, init_func=init, repeat=False, interval=mission_time)

        if vid:
            ani.save('harvest.mp4', writer=animation.FFMpegFileWriter(), fps=30)
        else:
            plt.show()
                

if __name__ == '__main__':
    ROBOT_CNT = 10
    robots = place_robots(ROBOT_CNT)
    field = SquareGrid(robots)
    points = [ (x,y) for x,y in robots ]
    circle = minidisk(frozenset(points), TaxicabCircle)
    mission_time = int( np.ceil(circle.r) )
    #mission_time *= 2

    goal = circle.center()
    agent = LogicalAgent(goal)
    #agent = RandomAgent(goal)
    animator = PrintAnimator(goal)
    harvester = Harvester(field, agent, mission_time, animator)
    harvester.play()
    print "Mission Time: ", mission_time
    print "Score: ", len(field.collected)
    print "% harvested: ", len(field.collected) / float(mission_time * ROBOT_CNT)
    animator.movietime(vid=False)