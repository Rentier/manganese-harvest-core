import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from harvest.visualize.visualizer import Visualizer

class PlotVisualizer(Visualizer):

    def visualize(self, **kwargs):
        self.do_animation(vid=False)

    def do_animation(self, vid=False, draw_paths=False):
        mission_time = self.t
        border = mission_time  + 5 
        xmid, ymid = self.goal
    
        fig  = plt.figure()
        axis = plt.gca() 
        robots, = axis.plot([], [], linestyle='none', marker='o', color='red', ms=3., zorder=42)
        harvested, = axis.plot([], [], linestyle='none', marker=',', color='black', ms=3., zorder=23) # Draw robots over mangan

        axis.set_xlim([xmid-border, xmid+border])    
        axis.set_ylim([ymid-border, ymid+border])
        axis.xaxis.set_visible(False)
        axis.yaxis.set_visible(False)

        t = np.arange(0, mission_time)
        
        patch = matplotlib.patches.RegularPolygon(self.goal, 4, radius=mission_time, color='g', animated=True, zorder=0, alpha=.1, lw=0, fc='c')    

        axis.set_aspect('equal')
        
        def init():
            robots.set_data([],[])
            harvested.set_data([],[])
            patch.center = self.goal
            patch.radius = mission_time
            axis.add_patch(patch)
            return robots, harvested, patch

        def animate(i):
            robots.set_data(self.positions_x[i], self.positions_y[i])
            if draw_paths:
                harvested.set_data(self.collected[i].transpose() if self.collected[i] is not None else ([], []))
            patch.radius = mission_time - i
            return robots, harvested, patch
            
        ani = animation.FuncAnimation(fig, animate, t, blit=True, init_func=init, repeat=False, interval=mission_time)

        plt.show()
            
