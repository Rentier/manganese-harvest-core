import math

best_path = []
best_path_value = 0
already_visited = set([(2,3), (3,3)])

#update best_path and best_path_value
def check_path(path):
    global best_path
    global best_path_value
    global already_visited
    path_value = len(set(path).difference(already_visited))
    if(path_value > best_path_value):
        best_path_value = path_value
        best_path = list(path)

#returns all neighbors (4 max) which are in reaching distance to the goal
def get_neighbors(node, goal, distance):
    neighbors = [(node[0] + 1, node[1]), (node[0], node[1] + 1), (node[0] - 1, node[1]), (node[0], node[1] - 1)]
    for n in list(neighbors):
        if math.fabs(n[0] - goal[0]) + math.fabs(n[1] - goal[1]) > distance:
            neighbors.remove(n)
    return neighbors

#recursive depth limited search with current node, goal and path length (depth)
def dls(node, goal, depth, path_so_far):
    if node == goal:
        path_so_far.append(node)
        check_path(path_so_far)
        path_so_far.pop()
    for n in get_neighbors(node, goal, depth - 1):
        path_so_far.append(node)
        dls(n, goal, depth - 1, path_so_far)
        path_so_far.pop()

#quick test     
if __name__ == "__main__":
    path = []
    start = (2, 2)
    goal = (2, 4)
    dls(start, goal, 4, path)
    print "Path with max value: " + str(best_path)
    print "Path value: " + str(best_path_value)
    
