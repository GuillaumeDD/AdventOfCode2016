import io
# From: http://www.redblobgames.com/pathfinding/a-star/implementation.html#python-dijkstra
import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

# --- Day 13: A Maze of Twisty Little Cubicles ---
# 
# You arrive at the first floor of this new building to discover a much
# less welcoming environment than the shiny atrium of the last
# one. Instead, you are in a maze of twisty little cubicles, all alike.
# 
# Every location in this area is addressed by a pair of non-negative
# integers (x,y). Each such coordinate is either a wall or an open
# space. You can't move diagonally. The cube maze starts at 0,0 and
# seems to extend infinitely toward positive x and y; negative values
# are invalid, as they represent a location outside the building. You
# are in a small waiting area at 1,1.
# 
# While it seems chaotic, a nearby morale-boosting poster explains, the
# layout is actually quite logical. You can determine whether a given
# x,y coordinate will be a wall or an open space using a simple system:
# 
#     Find x*x + 3*x + 2*x*y + y + y*y.
#     Add the office designer's favorite number (your puzzle input).
#     Find the binary representation of that sum; count the number of bits that are 1.
#         If the number of bits that are 1 is even, it's an open space.
#         If the number of bits that are 1 is odd, it's a wall.
# 
# For example, if the office designer's favorite number were 10, drawing
# walls as # and open spaces as ., the corner of the building containing
# 0,0 would look like this:
# 
#   0123456789
# 0 .#.####.##
# 1 ..#..#...#
# 2 #....##...
# 3 ###.#.###.
# 4 .##..#..#.
# 5 ..##....#.
# 6 #...##.###
# 
# Now, suppose you wanted to reach 7,4. The shortest route you could
# take is marked as O:
# 
#   0123456789
# 0 .#.####.##
# 1 .O#..#...#
# 2 #OOO.##...
# 3 ###O#.###.
# 4 .##OO#OO#.
# 5 ..##OOO.#.
# 6 #...##.###
# 
# Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).
# 
# What is the fewest number of steps required for you to reach 31,39?

with io.open('inputs/day13.txt') as f:
    INPUT = int(f.readlines()[0])

def is_space(n):
    """
    Find the binary representation of that sum; count the number of bits that are 1.
    If the number of bits that are 1 is even, it's an open space.
    If the number of bits that are 1 is odd, it's a wall.
    """
    binary_representation = bin(n)[2:]
    number_of_1 = len([c for c in binary_representation if c == '1'])
    return number_of_1 % 2 == 0

def magic_number(x, y):
    """
    Compute the magic number for a point (x, y)
    """
    global INPUT
    return x*x + 3*x + 2*x*y + y + y*y + INPUT

def neighbors(point):
    """
    Compute a list of neighor positions to visit
    """
    x, y = point
    result = []
    for n_x, n_y in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if n_x >= 0 and n_y >= 0: # only positive coordinates
            if is_space(magic_number(n_x, n_y)): # checking that it is a space
                result.append((n_x, n_y))

    return result

def search(x_from, y_from, x_to, y_to):
    """
    Dijkstra's algorithm to go from (x_from, y_from) to (x_to, y_to).

    It early stops once the destination is found (maps is infinite).
    """
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

steps = search(1, 1, 31, 39)
print('Going from {} to {} in {} steps'.format((1, 1), (31, 39), steps))


# --- Part Two ---
#
# How many locations (distinct x,y coordinates, including your starting
# location) can you reach in at most 50 steps?
#
def explore_max_steps(x_from, y_from, max_steps):
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
        
        for next_pos in neighbors(current_pos):
            new_cost = cost_so_far[current_pos] + 1
            
            if new_cost <= max_steps: # stop exploring it the cost exceeds max_steps
                if next_pos not in cost_so_far or new_cost < cost_so_far[current_pos]:
                    cost_so_far[next_pos] = new_cost
                    come_from[next_pos] = current_pos
                
                    priority = new_cost
                    frontier.put(next_pos, priority)

    return len(come_from)

nb_places = explore_max_steps(1, 1, 50)
print('It is possible to reach from {} within {} steps {} locations'.format((1, 1), 50, nb_places))
