from __future__ import division

import itertools

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import svgwrite
import png as libpng

from harvest.constants import *

def plot(data):
	min_x, min_y = np.min(data, axis=0)
	max_x, max_y = np.amax(data, axis=0)

	x_range = max_x - min_x
	y_range = max_y - min_y

	value_range = max(x_range, y_range)
	
	fig, axes = plt.subplots()
	axes.set_xlim([min_x-5, min_x+value_range+5])
	axes.set_ylim([min_y-5, min_x+value_range+5])	

	plt.axis('equal')
	
	# Draw distance circles
	for p in data:
		circle = plt.Circle(p,MAX_DISTANCE,color='g')
		fig.gca().add_artist(circle)
	
	plt.plot(*np.transpose(data), marker='o', color='r', ls='')
	plt.show(block=False)

def animated(data, goal, interval=200, paused=False):
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

	d = {'pause' : paused}

	def onClick(event):
	    d['pause'] ^= True
	
	def init():
		robots.set_data([],[])
		harvested.set_data([],[])
		patch.center = goal
		patch.radius = STEPS
		axis.add_patch(patch)
		return robots, harvested, patch

	def timez():
		t_max = STEPS - 1
		t = 0
		dt = 1
		while t < t_max:
			if not d['pause']:
				t = t + dt
			yield t			

	def animate(i):
		robots.set_data(data[i].T)
		patch.radius = STEPS - i
		return robots, harvested, patch
		
	fig.canvas.mpl_connect('button_press_event', onClick)
	ani = animation.FuncAnimation(fig, animate, timez, blit=True, init_func=init, repeat=True, interval=interval, )


	#ani.save('harvest.mp4', writer=animation.FFMpegFileWriter(), fps=30)
	plt.show(block=False)	


#http://bit.ly/19XGJCb
STATIC_COLORS = [
	"#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
	"#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
	"#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
	"#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
	"#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
	"#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
	"#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
	"#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",
	"#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
	"#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
	"#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
	"#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
	"#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
	"#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
	"#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
	"#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58" 
	]

def _normalize_positions(data):

	# Normalize
	min_x, min_y = np.min(data, axis=(0, 1))
	delta = np.array([min_x, min_y])
	data -= delta


def svg(points, filename):
	data = np.copy(points)
	_normalize_positions(data)
	
	# Find max of - normalized - data
	max_x, max_y = np.max(data, axis=(0, 1))

	size_str = "{}px"
	width = size_str.format(max_x + 1) 
	height = size_str.format(max_y + 1) 

	svg_document = svgwrite.Drawing(filename=filename, size=(height, width))

	positions_x, positions_y = data.T

	colors = itertools.cycle(STATIC_COLORS)

	for robot in zip(positions_y,positions_x):
		path = np.array(robot).T
		svg_document.add( svgwrite.shapes.Polyline(points=path, stroke_width="1", stroke = colors.next(),  fill="none"))

	svg_document.save()

def png(points,filename):

	def chunks(l, n):
		return [l[i:i+n] for i in range(0, len(l), n)]

	def color_to_rgb(c):
		return np.array([int(i,16) for i in chunks(c[1:], 2)])

	data = np.copy(points)
	_normalize_positions(data)
	max_x, max_y = np.max(data, axis=(0, 1))

	width = max_x + 1
	height = max_y + 1

	image_3d = np.zeros([height,width,3])
	image_3d.fill(255)

	positions_x, positions_y = data.T

	colors = itertools.cycle(STATIC_COLORS)

	for robot in zip(positions_x,positions_y):
		color = colors.next()
		path = np.array(robot).T
		for x,y in path:
			image_3d[y,x] = color_to_rgb(color)

	w = libpng.Writer(width,height)

	with open(filename, 'wb') as f:
		w.write(f, np.reshape(image_3d, (-1, width*3)))

	 


