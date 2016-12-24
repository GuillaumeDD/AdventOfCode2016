import io
# From: http://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra
import heapq
from itertools import permutations

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

# --- Day 24: Air Duct Spelunking ---
# 
# You've finally met your match; the doors that provide access to the
# roof are locked tight, and all of the controls and related electronics
# are inaccessible. You simply can't reach them.
# 
# The robot that cleans the air ducts, however, can.
# 
# It's not a very fast little robot, but you reconfigure it to be able
# to interface with some of the exposed wires that have been routed
# through the HVAC system. If you can direct it to each of those
# locations, you should be able to bypass the security controls.
# 
# You extract the duct layout for this area from some blueprints you
# acquired and create a map with the relevant locations marked (your
# puzzle input). 0 is your current location, from which the cleaning
# robot embarks; the other numbers are (in no particular order) the
# locations the robot needs to visit at least once each. Walls are
# marked as #, and open passages are marked as .. Numbers behave like
# open passages.
# 
# For example, suppose you have a map like the following:
# 
# ###########
# #0.1.....2#
# #.#######.#
# #4.......3#
# ###########
# 
# To reach all of the points of interest as quickly as possible, you
# would have the robot take the following path:
# 
#     0 to 4 (2 steps)
#     4 to 1 (4 steps; it can't move diagonally)
#     1 to 2 (6 steps)
#     2 to 3 (2 steps)
# 
# Since the robot isn't very fast, you need to find it the shortest
# route. This path is the fewest steps (in the above example, a total of
# 14) required to start at 0 and then visit every other location at
# least once.
# 
# Given your actual map, and starting from location 0, what is the
# fewest number of steps required to visit every non-0 number marked on
# the map at least once?


WALL = '#'
SPACE = '.'

MAP = []
POIs = {} # Points of interest, i.e. point 0, 1, 2, etc.

# Loading MAP and POIs
with io.open('inputs/day24.txt', 'r') as f:
    y = 0
    for line in f:
        MAP.append(line)
        x = 0
        for c in line:
            if c.isdigit():
                POIs[int(c)] = (x, y)
            x += 1

        y += 1

def width():
    """
    Width of the map
    """
    return len(MAP[0])

def height():
    """
    Height of the map
    """
    return len(MAP)

def get(x, y):
    """
    Return the element on the column x and the row y of the map
    """
    global MAP
    return MAP[y][x]

def is_space(x, y):
    """
    Determine if a point is a space
    """
    return get(x, y) != WALL

def neighbors(point):
    """
    Compute a list of neighor positions to visit
    """
    x, y = point
    result = []
    for n_x, n_y in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if n_x >= 0 and n_y >= 0 and n_x < width() and n_y < height(): 
            if is_space(n_x, n_y): 
                result.append((n_x, n_y))

    return result

def search(point_from, point_to):
    """
    Dijkstra's algorithm to go from (x_from, y_from) to (x_to, y_to).
    It early stops once the destination is found.
    """
    x_from, y_from = point_from
    x_to, y_to = point_to

    stop = (x_to, y_to)
    start = (x_from, y_from)

    frontier = PriorityQueue()
    frontier.put(start, 0)
    
    come_from = {}
    cost_so_far = {}

    come_from[start] = None
    cost_so_far[start] = 0

    found_stop = False
    steps = 0
    
    while not frontier.empty() and not found_stop:
        current_pos = frontier.get()

        # Early stop if necessary
        if current_pos == stop:
            steps = cost_so_far[current_pos]
            found_stop = True
        
        for next_pos in neighbors(current_pos):
            new_cost = cost_so_far[current_pos] + 1
            
            # Either:
            # - this is the first time this position is met, or
            # - this position is met a second time with a more direct path.
            #
            if next_pos not in cost_so_far or new_cost < cost_so_far[current_pos]:
                cost_so_far[next_pos] = new_cost
                come_from[next_pos] = current_pos
                
                priority = new_cost
                frontier.put(next_pos, priority)

    return steps

# Precomputation of distances from any POIs to another
distances = {}
for p1 in POIs.keys():
    distances[p1] = {}
    for p2 in POIs.keys():
        if p1 != p2:
            distances[p1][p2] = search(POIs[p1], POIs[p2])

# POIs except 0
points = [p for p in POIs.keys() if p != 0]

# Solving part 1
min_distance = None
for path in permutations(points):
    previous_point = 0
    distance = 0
    for p in path:
        distance += distances[previous_point][p]
        previous_point = p
    
    if min_distance is None:
        min_distance = distance
    else:
        min_distance = min(min_distance, distance)

print('Minimum distance is: {}'.format(min_distance))
            

# --- Part Two ---
# 
# Of course, if you leave the cleaning robot somewhere weird, someone is
# bound to notice.
# 
# What is the fewest number of steps required to start at 0, visit every
# non-0 number marked on the map at least once, and then return to 0?

min_distance = None
for path in permutations(points):
    path = list(path)
    path.append(0) # specific to part 2
    previous_point = 0
    distance = 0
    for p in path:
        distance += distances[previous_point][p]
        previous_point = p
    
    if min_distance is None:
        min_distance = distance
    else:
        min_distance = min(min_distance, distance)
print('Minimum distance is: {}'.format(min_distance))
