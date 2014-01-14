import numpy as np
import itertools

import ttk
from Tkinter import *
import tkFileDialog
import tkMessageBox
import tkSimpleDialog

import os.path
import sys

from harvest.util import abstract

import fharvest.logic as fhl

from harvest.place_robots import place_robots
from harvest.geometry.taxicab_circle import TaxicabCircle
from harvest.geometry.minidisk import minidisk

from harvest.visualize import *

import harvest.io as io

from harvest.distance import *
from harvest.constants import MAX_DISTANCE

def distance_constraint_holds(robots):
	N = len(robots)
	distances = np.empty([N,N])
	for x in xrange(N):
		for y in xrange(N):
			if x != y:
				distances[x,y] = euclidean_distance(robots[x], robots[y])
			else:
				distances[x,y] = -1

	for n in xrange(N):
		valid = any(0 <= x <= MAX_DISTANCE for x in distances[n]  )
		if not valid:
			print n
			print distances[n]
			return False

	return True

def all_can_reach_goal(robots, goal, t):
	for robot in robots:
		if taxicab_distance(robot, goal) > t:
			return False
	return True

def goal_was_reached(data, goal):
	for robot in data[-1]:
		if not np.array_equal(robot, GOAL):
			return False
	return True

def calc_battle_plan(robots):
	while True:
		points = [ (x,y) for x,y in robots ]
		circle = minidisk(frozenset(points), TaxicabCircle)
		MISSION_TIME = int( np.ceil(circle.r) ) + 1
		GOAL =  np.rint(circle.center()).astype(int)

		if all_can_reach_goal(robots, GOAL, MISSION_TIME):
			return GOAL, MISSION_TIME	

def simulate(robots, robo_count, doubletime=False):
	AGENT = "heuristic"
	assert distance_constraint_holds(robots)

	GOAL, MISSION_TIME = calc_battle_plan(robots)
	assert all_can_reach_goal(robots, GOAL, MISSION_TIME)

	if doubletime:
		MISSION_TIME *= 2

	STEPS = MISSION_TIME + 1	
	GOAL_X, GOAL_Y = GOAL
	
	data = np.zeros([STEPS, robo_count, 2], dtype=np.int32)
	data[0] = robots

	traveled, collected = fhl.harvest(data, AGENT, GOAL_X, GOAL_Y, STEPS, robo_count)
	#assert goal_was_reached(data, GOAL)

	print "Double: ", doubletime
	print "Robots: ", robo_count
	print "Mission time: ", MISSION_TIME 
	print "Goal: ", GOAL
	print "Traveled: ", traveled
	print "Collected: ", collected
	print "% harvested: ", collected / float(MISSION_TIME * robo_count)

	
	FILENAME = "test_{}_{}".format(robo_count, AGENT)
	if doubletime: FILENAME += "_double"

	#animated(data,GOAL,interval=100)
	#svg(data, FILENAME + ".svg")
	#png(data, FILENAME + ".png")

	return data, int(traveled), int(collected), GOAL

class GuiState(object):

	def __init__(self):
		self.robo_count = None
		self.positions = None

		self.data_single = None
		self.collected_single = None
		self.traveled_single = None
		self.goal_single = None

		self.data_double = None
		self.collected_double = None
		self.traveled_double = None
		self.goal_double = None

	def load_constant(self, path):
		self.robo_count = io.constant_from_file(path)

	def load_positions(self, path):
		self.robo_count, self.positions = io.positions_from_file(path)

	def save_positions(self, path):
		io.positions_to_file(path, self.positions)

	def generate_positions(self):
		self.positions = place_robots(self.robo_count)

	def simulate(self):
		self.data_single, self.traveled_single, self.collected_single, self.goal_single = simulate(self.positions, self.robo_count)
		self.data_double, self.traveled_double, self.collected_double, self.goal_double = simulate(self.positions, self.robo_count, doubletime=True)

	def visualize(self, media, path):
		if "animate" in media: 
			animated(self.data_single, self.goal_single, title="Single time")
			animated(self.data_double, self.goal_double, paused=True, title="Double time")
		if "svg" in media: 
			svg(self.data_single, path + "_single.svg")
			svg(self.data_double, path + "_double.svg")
		if "png" in media: 
			png(self.data_single, path + "_single.png")
			png(self.data_double, path + "_double.png")
		if "mov" in media: 
			animated(self.data_single, self.goal_single, path=path+"_single.mp4")
			animated(self.data_double, self.goal_single, path=path+"_double.mp4")
		if "positions" in media: 
			io.positions_to_file(path + "_positions.txt", self.positions)


		tkMessageBox.showinfo("Success", "Data has been visualized!")

	def plot_positions(self):
		plot(self.positions)

state = GuiState()		

class View(object):

	def __init__(self, on_next, on_close):
		self.frame = ttk.Frame()
		self.on_next = on_next
		self.on_close = on_close

	def pack(self, **kwargs):
		abstract()

	def pack_forget(self):
		self.frame.pack_forget()

	def generate_positions(self):
		while state.robo_count is None:
			state.robo_count = tkSimpleDialog.askinteger("Robo count", "How many robots?\n Valid are integers [0,150].\nValues above 100 are not recommended!", minvalue=1, maxvalue=200)
		print state.robo_count
		state.generate_positions()
		self.on_next("pos_created")

	def simulate(self):
		state.simulate()
		s = "{}:\nCollected: {} kg \nTraveled: {} m\n"
		msg = "Simulation has been finished:\n"
		msg += s.format("Single time", state.collected_single, state.traveled_single)
		msg += s.format("Double time", state.traveled_double, state.collected_double)
		tkMessageBox.showinfo("Success", msg)
		self.on_next("simulated")

	def close(self):
		self.on_close()

	def restart(self):
		self.on_next("entry")

class EntryView(View):

	def __init__(self, on_next, on_close):
		super(EntryView, self).__init__(on_next, on_close)

		master = self.frame

		header = ttk.Label(master, text="Welcome to the Pacific!",)
		header.pack(padx=10, pady=10)

		btn_frame = ttk.Label(master)
		btn_frame.pack()

		generate_positions_btn = ttk.Button(btn_frame, text="Generate positions", command=self.generate_positions)
		generate_positions_btn.pack(expand=1,fill=X)

		load_positions_btn = ttk.Button(btn_frame, text="Load positions from file", command=self.load_positions)
		load_positions_btn.pack(expand=1,fill=X)

		load_constant_btn = ttk.Button(btn_frame, text="Load constant from file", command=self.load_constant)
		load_constant_btn.pack(expand=1,fill=X)		

	def pack(self, **kwargs):
		self.frame.pack(**kwargs)

	def load_positions(self):
		print "Loading positions"
		path = tkFileDialog.askopenfilename()
		state.load_positions(path)
		tkMessageBox.showinfo("Success", "Positions have been loaded: \n{} robots.".format(state.robo_count))
		self.on_next("pos_created") 

	def load_constant(self):
		path = tkFileDialog.askopenfilename()
		state.load_constant(path)
		tkMessageBox.showinfo("Success", "Constant has been loaded: \n{} robots.".format(state.robo_count))
		self.on_next("const_loaded")		

class PositionsCreatedView(View):

	def __init__(self, on_next, on_close):
		super(PositionsCreatedView, self).__init__(on_next, on_close)

		master = self.frame

		header = ttk.Label(master, text="Position data has arrived. How to proceed?")
		header.pack(padx=10, pady=10)

		btn_frame = ttk.Label(master)
		btn_frame.pack()

		simulate_btn = ttk.Button(btn_frame, text="Simulate", command=self.simulate)
		simulate_btn.pack()

		save_positions_btn = ttk.Button(btn_frame, text="Save positions", command=self.save_positions)
		save_positions_btn.pack()

		show_positions_btn = ttk.Button(btn_frame, text="Show positions", command=self.show_positions)
		show_positions_btn.pack()

	def pack(self, **kwargs):
		self.frame.pack(**kwargs)

	def show_positions(self):
		state.plot_positions()

	def save_positions(self):
		print "Positions saved"
		path = tkFileDialog.asksaveasfilename()
		state.save_positions(path)
		tkMessageBox.showinfo("Success", "Positions have been saved!")
		self.on_next("pos_created")

class ConstantLoadedView(View):

	def __init__(self, on_next, on_close):
		super(ConstantLoadedView, self).__init__(on_next, on_close)

		master = self.frame

		header = ttk.Label(master, text="Constant has been loaded. How to proceed?",)
		header.pack(padx=10, pady=10 )

		generate_positions_btn = ttk.Button(master, text="Generate positions", command=self.generate_positions)
		generate_positions_btn.pack()	

	def pack(self, **kwargs):
		self.frame.pack(**kwargs)

class PositionsWrittenView(View):

	def __init__(self, on_next, on_close):
		super(PositionsWrittenView, self).__init__(on_next, on_close)

		master = self.frame

		header = ttk.Label(master, text="Positions haven been saved. How to proceed?")
		header.pack()

		simulate_btn = ttk.Button(master, text="Simulate", command=self.simulate)
		simulate_btn.pack()

	def pack(self, **kwargs):
		self.frame.pack(**kwargs)	

class SimulatedView(View):

	def __init__(self, on_next, on_close):
		super(SimulatedView, self).__init__(on_next, on_close)

		master = self.frame

		header = ttk.Label(master, text="Stuff has been simulated. How to proceed?")
		header.pack()

		group = ttk.LabelFrame(master, text="Visualize")

		self.option_plt = BooleanVar()
		self.option_svg = BooleanVar()
		self.option_png = BooleanVar()
		self.option_mov = BooleanVar()
		self.option_pos = BooleanVar()

		Checkbutton(master, text="Show animation", variable=self.option_plt).pack()
		Checkbutton(master, text="Write positions  ", variable=self.option_pos).pack()
		Checkbutton(master, text="Export svg        ", variable=self.option_svg).pack()
		Checkbutton(master, text="Export png       ", variable=self.option_png).pack()
		Checkbutton(master, text="Export mp4      ", variable=self.option_mov).pack()

		group.pack()

		btn_frame = ttk.Label(master)
		btn_frame.pack()

		visualize_btn = ttk.Button(btn_frame, text="Visualize", command=self.visualize)
		visualize_btn.pack()

		restart_btn = ttk.Button(btn_frame, text="Restart", command=self.restart)
		restart_btn.pack()

	def pack(self, **kwargs):
		self.frame.pack(**kwargs)

	def visualize(self):
		media = []
		need_name = False
		if self.option_plt.get(): media.append("animate");
		if self.option_svg.get(): media.append("svg"); need_name = True
		if self.option_png.get(): media.append("png"); need_name = True
		if self.option_mov.get(): media.append("mov"); need_name = True
		if self.option_pos.get(): media.append("positions"); need_name = True

		name = None
		if need_name:
			formats = [ ('File Name','*') ]
			name = tkFileDialog.asksaveasfilename(parent=None,filetypes=formats ,title="Directory and asename of visualization files is... ")

		state.visualize(media, name)

		self.on_next("simulated")

class Wizard(ttk.Frame):
	def __init__(self, master=None, **kw):
		ttk.Frame.__init__(self, master,)

		self.views = { 
						"entry" : EntryView(self.next_page, self.close),
		            	"pos_created" : PositionsCreatedView(self.next_page, self.close),
		            	"const_loaded" : ConstantLoadedView(self.next_page, self.close),
		            	"pos_written" : PositionsWrittenView(self.next_page, self.close),
		            	"simulated" : SimulatedView(self.next_page, self.close),
		             }


		self.current = "entry"

		self.views[self.current].pack(expand=1,fill='both')

	def next_page(self, s):
		self.pack_forget()
		self.views[self.current].pack_forget()
		self.current = s
		self.views[self.current].pack(expand=1,fill='both')
		
		print s

	def close(self):
		print "Close"
		self.master.destroy()
		sys.exit(0)

def demo():
	root = Tk()
	root.wm_title("Mangani sacra fames")
	root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
	s = ttk.Style()
	s.theme_use('clam')
	wizard = Wizard()
	wizard.master.minsize(300, 200)
	wizard.master
	wizard.pack(expand=1,fill='both')

	root.mainloop()

if __name__ == "__main__":
	demo()