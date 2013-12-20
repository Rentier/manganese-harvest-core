if __name__ == '__main__':
		
	import matplotlib.pyplot as plt
        import matplotlib
        import numpy as np

	from harvest.geometry.taxicab_circle import TaxicabCircle
        from harvest.geometry.minidisk import minidisk

	c_min = -1000
	c_max = 1000
	
	def random_set_of_points(num):
		""" Creates a frozenset sized num of random 2D points """
		result = []
		for unused in range(num):
			[[x,y]] = np.random.random_integers(c_min,c_max,[1,2])
			result.append( (x,y) )
		return frozenset(result)

	def plot_minidisk(data, circle):
		fig, axes = plt.subplots(figsize=(6,6))
		axes.set_ylim([c_min * 1.4, c_max * 1.4])
		axes.set_xlim([c_min * 1.4, c_max * 1.4])
		
		size = 2 * circle.radius()
		circ_x, circ_y = circle.center()
		diagonal = np.sqrt( 2 * size ** 2) / 2
		rect = matplotlib.patches.Rectangle((circ_x , circ_y - size/2), diagonal , diagonal, angle=45., color='g')
		
		plt.plot(*np.transpose(data), marker='o', color='r', ls='')
		plt.plot(*np.transpose([circle.center()]), marker='o', color='b', ls='')
		fig.gca().add_artist(rect)
		plt.show()

	points = random_set_of_points(100)
	circle = minidisk(points, TaxicabCircle)
	plot_minidisk(np.array(list(points)), circle)
