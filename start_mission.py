from harvest.agents import *
from harvest.environments import *

from harvest.harvester import Harvester
from harvest.place_robots import generate_data
from harvest.circle_magic import minidisk

import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
        line, = axis.plot([], [], linestyle='none', marker='o', color='r', zorder=42)

        axis.set_xlim([xmid-border, xmid+border])    
        axis.set_ylim([ymid-border, ymid+border])

        time_template = 'time = %.1fs'
        text = plt.text(0.1, 0.9,'matplotlib', ha='center', va='center')

        t = np.arange(0, mission_time)
        patch = plt.Circle(self.goal, mission_time, fc='c', animated=True, lw=0, zorder=0, alpha=.1)

        axis.set_aspect('equal')
        
        def init():
            line.set_data([],[])
            text.set_text('')
            patch.center = self.goal
            patch.radius = mission_time
            axis.add_patch(patch)
            return line, text, patch

        def animate(i):
            line.set_data(self.x[i],self.y[i])
            text.set_text(time_template.format(mission_time-i))
            patch.radius = mission_time - i
            return line, text, patch
            

        ani = animation.FuncAnimation(fig, animate, t, blit=True, init_func=init, repeat=False, interval=mission_time)

        if vid:
            ani.save('harvest.mp4', writer=animation.FFMpegFileWriter(), fps=30)
        else:
            plt.show()
                

if __name__ == '__main__':
    robots = generate_data(10)
    field = SquareGrid(robots)
    points = [ (x,y) for x,y in robots ]
    circle = minidisk(frozenset(points))
    mission_time = int( np.ceil(circle.r) + 1)
    agent = RandomAgent(circle.center())
    animator = PrintAnimator(circle.center())
    harvester = Harvester(field, agent, mission_time, animator)
    harvester.play()
    animator.movietime(vid=True)
    