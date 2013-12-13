"""Mangan Harvest CLI

Usage:
  harvest_cli.py read number <file>
  harvest_cli.py read positions <file>
  harvest_cli.py write positions <file>
  harvest_cli.py write mission <file>
  harvest_cli.py (-h | --help)

Read number:
  The data format used for 'read number' consists
  of a single line, which contains an integer C
  with 0 < C <= 100.

  An example for a valid input file:

  42

Read positions:
  The first line describes the number c of robots.
  After that, the next c lines are coordinates for
  the robots in the format  x y . Valid values for
  x and y are non-negative integers.

  An example for a valid input file:

  3
  0 0
  1 1
  2 1

Write positions:

  Same file format as 'Read positions'.

Write mission:
  TODO

Options:
  -h --help      Show this screen.
"""
import numpy as np
import csv

from docopt import docopt

from place_robots import generate_data

def read_number(path):
    with open(path, 'r') as f:
        N = f.readline()
    return int(N)

def read_positions(path):
    with open(path, 'r') as f:
        N = int(f.readline())
        positions = np.zeros((N,2), int)
        reader = csv.reader(f, delimiter=' ')
        for i, row in enumerate(reader):
            positions[i][0] = int(row[0])
            positions[i][1] = int(row[1])
    return positions        

if __name__ == "__main__":
    arguments = docopt(__doc__)
    path = arguments['<file>']
    if arguments['read']:
        if arguments['number']:
            i = read_number(path)
            print(i)
        elif arguments['positions']:
            positions = read_positions(path)
            print(positions)
    elif arguments['write']:
        if arguments['number']:
            pass
        elif arguments['positions']:
            pass
    
        