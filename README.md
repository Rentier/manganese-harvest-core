mangan-harvest
=============

Design Goal
-----------

Keeping it as simple as possible:

* Choose naive/most easiest solution first, until further requirements demand for more complex
* Make it extensible/modular so changes come at nearly no cost

## Modelling of the Pacific Ocean Bed

### World

* World is divided into polygon tiles identified by x and y non-negative integer coordinates
* In the first version, squares are chosen as tile shape
* Each tile has a base of 1m
* Data structure to store the world is a set of points of already visited tiles. That implies that only points in there have been freed of mangan, all other are still harvestable

![Grid of the world][world-grid]

#### Possible future improvements

*  Hexagons are an improvement to think of, since the error of sucking a circle area in a polyon cell is smaller with them. Guide to them can be found here: http://www.redblobgames.com/grids/hexagons/

#### Discarded ideas

* Datas structure to store the world is a grid of size (N*200)^2
* No integer coordinates, but real numbers

### Robots

* There are N robots
* A robot is a simple 2-D vector [x,y]
* Robots are stored in a list. 

#### Possible future improvements

* Space-partitioning data structures like kd-tree or quad tree

### Updating

Time is discretized in seconds, since robots move with 1m/s. After every delta, each robot can move into a neighbouring cell instantaniously. He sucks then everything in there.

### Navigation

Every robot knows the relative distance to each other robot

Solution
----------
* Vielleicht vergleichbar mit  Computer Go (viele Zustände, wird mit zunehmender Spieldauer komplexer, nicht wie Schach, einfacher)
* Good Old Fashioned AI (GOFAI), wie Min-Max, Alpha-Beta, ist schwierig, da extrem hoher Branching-Faktor, und wird mit großer Anzahl an Robotern immer schlimmer

Ideen
-----

### Tree search

#### Pro

* Easy

#### Contra

* Slow, since many states
* Memory hungry, since branching factor
* Maybe bad results, since branching factor

### Monte Carlo methods

#### Pro

* Easy

#### Contra

* Slow, since many states
* Memory hungry, since branching factor
* Maybe bad results, since branching factor, but still better than tree search

### Pattern matching

#### Pro

#### Contra

### The creation of knowledge-based systems

#### Pro

#### Contra

* No expert to create knowledge

### The use of machine learning

#### Pro

#### Contra

* More complex



[world-grid]: http://www-cs-students.stanford.edu/~amitp/game-programming/grids/square-grid-face-coordinates.png "Square grid"
