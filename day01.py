import io


# --- Day 1: No Time for a Taxicab ---
#
# Santa's sleigh uses a very high-precision clock to guide its
# movements, and the clock's oscillator is regulated by
# stars. Unfortunately, the stars have been stolen... by the Easter
# Bunny. To save Christmas, Santa needs you to retrieve all fifty stars
# by December 25th.
#
# Collect stars by solving puzzles. Two puzzles will be made available
# on each day in the advent calendar; the second puzzle is unlocked when
# you complete the first. Each puzzle grants one star. Good luck!
#
# You're airdropped near Easter Bunny Headquarters in a city
# somewhere. "Near", unfortunately, is as close as you can get - the
# instructions on the Easter Bunny Recruiting Document the Elves
# intercepted start here, and nobody had time to work them out further.
#
# The Document indicates that you should start at the given coordinates
# (where you just landed) and face North. Then, follow the provided
# sequence: either turn left (L) or right (R) 90 degrees, then walk
# forward the given number of blocks, ending at a new intersection.
#
# There's no time to follow such ridiculous instructions on foot,
# though, so you take a moment and work out the destination. Given that
# you can only walk on the street grid of the city, how far is the
# shortest path to the destination?
#
# For example:
#
#     Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
#     R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
#     R5, L5, R5, R3 leaves you 12 blocks away.
#
# How many blocks away is Easter Bunny HQ?
#
# --- Part Two ---
#
# Then, you notice the instructions continue on the back of the
# Recruiting Document. Easter Bunny HQ is actually at the first location
# you visit twice.
#
# For example, if your instructions are R8, R4, R4, R8, the first
# location you visit twice is 4 blocks away, due East.
#
# How many blocks away is the first location you visit twice?
#

NORTH = 'North'
EAST = 'East'
WEST = 'West'
SOUTH = 'South'

def change_degree(degree, direction):
    """
    Compute the new degree given the current degree (NORTH, EAST, WEST or SOUTH)
    and a direction (either 'L' or 'R')
    """
    if degree == NORTH:
        if direction == 'L':
            return WEST
        elif direction == 'R':
            return EAST
    elif degree == EAST:
        if direction == 'L':
            return NORTH
        elif direction == 'R':
            return SOUTH
    elif degree == WEST:
        if direction == 'L':
            return SOUTH
        elif direction == 'R':
            return NORTH
    elif degree == SOUTH:
        if direction == 'L':
            return EAST
        elif direction == 'R':
            return WEST

with io.open('inputs/day01.txt','r') as f:
    # Obtaining instruction
    instructions = [instruct.strip() for instruct in f.readline().split(', ') if len(instruct.strip()) > 0]

    # Initialisation of coordinates on the grid
    x, y = 0, 0
    degree = NORTH

    # Initisalition of the history of locations
    last_locations = set()
    last_locations.add((x,y))
    location_visited_twice = None
    def add_location(x, y):
        """
        Helper function to add a location to history and keep track
        of the first visited twice location
        """
        global location_visited_twice
        # Checking if the position has already been visited
        if (x,y) in last_locations and location_visited_twice is None:
            location_visited_twice = (x,y)
        # Updating the history of positions
        last_locations.add((x,y))
        
    # Moving process
    for inst in instructions:
        # Determination of the instructions
        move = inst[0]
        quantity = int(inst[1:]) # beware: quantity may be on several digits

        # Computation of new coordinates
        degree = change_degree(degree, move)

        if degree == NORTH:
            for _ in range(quantity):
                y += 1
                add_location(x, y)

        elif degree == WEST:
            for _ in range(quantity):
                x -= 1
                add_location(x, y)

        elif degree == SOUTH:
            for _ in range(quantity):
                y -= 1
                add_location(x, y)

        elif degree == EAST:
            for _ in range(quantity):
                x += 1
                add_location(x, y)

    # PART 1
    # Computing shortest path
    result = abs(x) + abs(y)
    print('[part1] Shortest path from (0,0) to {} is {}'.format((x,y),result))

    # PART 2
    (x, y) = location_visited_twice
    result = abs(x) + abs(y)
    print('[part2] First location visited twice is {}, dist={}'.format(location_visited_twice, result))



