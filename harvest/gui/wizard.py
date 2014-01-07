import ttk
from Tkinter import *
import tkFileDialog

from harvest.util import abstract


class View(object):

	def __init__(self, on_next, on_prev, on_close):
		self.frame = ttk.Frame()
		self.on_next = on_next
		self.on_prev = on_prev
		self.on_close = on_close

	def grid(self, **kwargs):
		abstract()

	def grid_forget(self):
		self.frame.grid_forget()

	def close(self):
		self.on_close()

class EntryView(View):

	def __init__(self, on_next, on_prev, on_close):
		super(EntryView, self).__init__(on_next, on_prev, on_close)

		master = self.frame

		header = ttk.Label(master, text="Welcome to the Pacific!",)
		header.grid(row=0, column=0, sticky=E+W, padx=10, pady=10 )

		generate_positions_btn = ttk.Button(master, text="Generate positions", command=self.generate_positions)
		generate_positions_btn.grid(row=1, column=0, sticky=E+W)

		load_positions_btn = ttk.Button(master, text="Load positions from file", command=self.load_positions)
		load_positions_btn.grid(row=2, column=0, sticky=E+W)

		load_constant_btn = ttk.Button(master, text="Load constant from file", command=self.load_constant)
		load_constant_btn.grid(row=3, column=0, sticky=E+W)		

	def grid(self, **kwargs):
		self.frame.grid(**kwargs)

	def generate_positions(self):
		print "Generate positions"
		self.on_next("pos_created") 

	def load_positions(self):
		print "Loading positions"
		self.on_next("pos_created") 

	def load_constant(self):
		self.on_next("const_loaded")	

class ConstantLoadedView(View):

	def __init__(self, on_next, on_prev, on_close):
		super(ConstantLoadedView, self).__init__(on_next, on_prev, on_close)

		master = self.frame

		constant = 42

		header = ttk.Label(master, text="Constant has been loaded. Value is",)
		header.grid(row=0, column=0, sticky=E+W, padx=10, pady=10 )

		constant_label = ttk.Label(master, text=str(constant))
		constant_label.grid(row=1, column=0, sticky=E+W, padx=20, pady=20 )

		generate_positions_btn = ttk.Button(master, text="Generate positions", command=self.generate_positions)
		generate_positions_btn.grid(row=2, column=0, sticky=E+W)	

	def grid(self, **kwargs):
		self.frame.grid(**kwargs)

	def generate_positions(self):
		print "Generate positions"
		self.on_next("pos_created")	

class PositionsCreatedView(View):

	def __init__(self, on_next, on_prev, on_close):
		super(PositionsCreatedView, self).__init__(on_next, on_prev, on_close)

		master = self.frame

		header = ttk.Label(master, text="Position data has arrived. How to proceed?")
		header.grid(row=0, sticky=E+W)

		simulate_btn = ttk.Button(master, text="Simulate", command=self.simulate)
		simulate_btn.grid(row=1, sticky='s')

		save_positions_btn = ttk.Button(master, text="Save positions", command=self.simulate)
		save_positions_btn.grid(row=2, sticky='s')

	def grid(self, **kwargs):
		self.frame.grid(**kwargs)

	def simulate(self):
		self.on_next("simulated")

	def save_positions(self):
		print "Positions saved"
		self.on_next("pos_written")
		

class PositionsWrittenView(View):

	def __init__(self, on_next, on_prev, on_close):
		super(PositionsWrittenView, self).__init__(on_next, on_prev, on_close)

		master = self.frame

		header = ttk.Label(master, text="Positions haven been saved. How to proceed?")
		header.grid(row=0, sticky=E+W)

		simulate_btn = ttk.Button(master, text="Simulate", command=self.simulate)
		simulate_btn.grid(row=1, sticky='s')

	def grid(self, **kwargs):
		self.frame.grid(**kwargs)

	def simulate(self):
		self.on_next("simulated")	

class SimulatedView(View):

	def __init__(self, on_next, on_prev, on_close):
		super(SimulatedView, self).__init__(on_next, on_prev, on_close)

		master = self.frame

		header = ttk.Label(master, text="Stuff has been simulated. How to proceed?")
		header.grid(row=0, sticky=E+W)

		group = ttk.LabelFrame(master, text="Visualize")

		option_plt = IntVar()
		option_svg = IntVar()
		option_png = IntVar()
		option_mov = IntVar()
		option_pos = IntVar()

		Checkbutton(group, text="Plot", variable=option_plt).grid(row=0, column=0, sticky=W)
		Checkbutton(group, text="Write positions", variable=option_pos).grid(row=1, column=0, sticky=W)
		Checkbutton(group, text="Export svg", variable=option_svg).grid(row=2, column=0, sticky=W)
		Checkbutton(group, text="Export png", variable=option_png).grid(row=3, column=0, sticky=W)
		Checkbutton(group, text="Export mp4", variable=option_mov).grid(row=4, column=0, sticky=W)

		group.grid(row=1, sticky=E+W)

		visualize_btn = ttk.Button(master, text="Visualize", command=self.visualize)
		visualize_btn.grid(row=2, sticky=W)

		finish_btm = ttk.Button(master, text="Finish", command=self.close)
		finish_btm.grid(row=2, sticky=E)

	def grid(self, **kwargs):
		self.frame.grid(**kwargs)

	def visualize(self):
		formats = [ ('File Name','*') ]

		name = tkFileDialog.asksaveasfilename(parent=None,filetypes=formats ,title="Save the image as...")
		print name
		self.on_next("simulated")



class Wizard(ttk.Frame):
	def __init__(self, master=None, **kw):
		ttk.Frame.__init__(self, master,)

		self.views = { 
						"entry" : EntryView(self.next_page, self.prev_page, self.close),
		            	"pos_created" : PositionsCreatedView(self.next_page, self.prev_page, self.close),
		            	"const_loaded" : ConstantLoadedView(self.next_page, self.prev_page, self.close),
		            	"pos_written" : PositionsWrittenView(self.next_page, self.prev_page, self.close),
		            	"simulated" : SimulatedView(self.next_page, self.prev_page, self.close),
		             }

		self.current = "entry"
		self.views[self.current].grid()

	def next_page(self, s):
		self.views[self.current].grid_forget()
		self.current = s
		self.views[self.current].grid(sticky=N+S+E+W)
		print s

	def prev_page(self, s):
		print "prev"

	def close(self):
		self.master.destroy()

def demo():
	root = Tk()
	root.wm_title("Mangani sacra fames")
	s = ttk.Style()
	s.theme_use('clam')
	wizard = Wizard()
	wizard.master.minsize(300, 200)
	wizard.grid(sticky=N+S+E+W)
	root.mainloop()

if __name__ == "__main__":
	demo()