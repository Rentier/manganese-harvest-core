import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot(data, goal, interval=200):
	STEPS = data.shape[0]
	border = STEPS  + 5 
	xmid, ymid = goal

	fig  = plt.figure()
	axis = plt.gca() 
	robots, = axis.plot([], [], linestyle='none', marker='o', color='red', ms=3., zorder=42)
	harvested, = axis.plot([], [], linestyle='none', marker=',', color='black', ms=3., zorder=23) # Draw robots over mangan

	axis.set_xlim([xmid-border, xmid+border])    
	axis.set_ylim([ymid-border, ymid+border])
	axis.xaxis.set_visible(False)
	axis.yaxis.set_visible(False)

	t = np.arange(0, STEPS)
	
	patch = matplotlib.patches.RegularPolygon(goal, 4, radius=STEPS, color='g', animated=True, zorder=0, alpha=.1, lw=0, fc='c')    

	axis.set_aspect('equal')
	
	def init():
		robots.set_data([],[])
		harvested.set_data([],[])
		patch.center = goal
		patch.radius = STEPS
		axis.add_patch(patch)
		return robots, harvested, patch

	def animate(i):
		robots.set_data(data[i].T)
		patch.radius = STEPS - i
		return robots, harvested, patch
		
	ani = animation.FuncAnimation(fig, animate, t, blit=True, init_func=init, repeat=False, interval=interval)


	#ani.save('harvest.mp4', writer=animation.FFMpegFileWriter(), fps=30)
	plt.show()	