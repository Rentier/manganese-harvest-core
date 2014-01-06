import ttk
from Tkinter import *

from harvest.util import abstract


class View(object):

	def __init__(self, on_next, on_prev):
		self.frame = ttk.Frame()
		self.on_next = on_next
		self.on_prev = on_prev

	def grid(self, **kwargs):
		abstract()

	def grid_forget(self):
		self.frame.grid_forget()

class EntryView(View):

	def __init__(self, on_next, on_prev):
		super(EntryView, self).__init__(on_next, on_prev )

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

	def __init__(self, on_next, on_prev):
		super(ConstantLoadedView, self).__init__(on_next, on_prev )

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

	def __init__(self, on_next, on_prev):
		super(PositionsCreatedView, self).__init__(on_next, on_prev )

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
		self.on_next("positions_saved")

	def save_positions(self):
		print "Positions saved"

class Wizard(ttk.Frame):
	def __init__(self, master=None, **kw):
		ttk.Frame.__init__(self, master,)

		self.views = { 
						"entry" : EntryView(self.next_page, self.prev_page),
		            	"pos_created" : PositionsCreatedView(self.next_page, self.prev_page),
		            	"const_loaded" : ConstantLoadedView(self.next_page, self.prev_page)
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
	wizard = Wizard()
	#wizard.master.minsize(400, 350)
	wizard.grid(sticky=N+S+E+W)
	root.mainloop()

if __name__ == "__main__":
	demo()