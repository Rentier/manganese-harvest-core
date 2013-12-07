import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from circle_magic import *



c_min = -10
c_max = 10

def plot(data, circle):
    fig, axes = plt.subplots(figsize=(6,6))
    axes.set_ylim([c_min * 1.4, c_max * 1.4])
    axes.set_xlim([c_min * 1.4, c_max * 1.4])
    
    plt.plot(*np.transpose(data), marker='o', color='r', ls='')
    plt.plot(*np.transpose([circle.center()]), marker='o', color='b', ls='')
    disk = plt.Circle(circle.center(),circle.r,color='g')
    fig.gca().add_artist(disk)
    plt.show()
    
def two_points_example():
    p1, p2 = np.random.random_integers(c_min,c_max,[2,2])
    circle = Circle.from_two_points(p1, p2)
    plot([p1,p2], circle)

def three_points_example():
    p1, p2, p3 = np.random.random_integers(c_min,c_max,[3,2])
    circle = Circle.from_three_points(p1, p2, p3)
    plot([p1,p2,p3], circle)
    
def random_set_of_points(num):
    """ Creates a frozenset sized num of random 2D points """
    result = []
    for unused in range(num):
        [[x,y]] = np.random.random_integers(c_min,c_max,[1,2])
        result.append( (x,y) )
    return frozenset(result)

points = random_set_of_points(100)
circle = minidisk(points)
plot(np.array(list(points)), circle)
    
if __name__ == "__main__":
	#two_points_example()
	three_points_example()
