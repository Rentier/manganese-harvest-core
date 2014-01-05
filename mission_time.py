from harvest.geometry.minidisk import minidisk
from harvest.geometry.taxicab_circle import TaxicabCircle

from harvest.io import *

files = ['tests/robots_010.txt',
         'tests/robots_020.txt',
         'tests/robots_100.txt']

for path in files:
    robots = positions_from_file(path)
    points = [ (x,y) for x,y in robots ]
    circle = minidisk(frozenset(points), TaxicabCircle)
    print path, circle.radius(), [int(x) for x in circle.center()]

