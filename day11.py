from itertools import combinations
import heapq

# --- Day 11: Radioisotope Thermoelectric Generators ---
# 
# You come upon a column of four floors that have been entirely sealed
# off from the rest of the building except for a small dedicated
# lobby. There are some radiation warnings and a big sign which reads
# "Radioisotope Testing Facility".
# 
# According to the project status board, this facility is currently
# being used to experiment with Radioisotope Thermoelectric Generators
# (RTGs, or simply "generators") that are designed to be paired with
# specially-constructed microchips. Basically, an RTG is a highly
# radioactive rock that generates electricity through heat.
# 
# The experimental RTGs have poor radiation containment, so they're
# dangerously radioactive. The chips are prototypes and don't have
# normal radiation shielding, but they do have the ability to generate
# an elecromagnetic radiation shield when powered. Unfortunately, they
# can only be powered by their corresponding RTG. An RTG powering a
# microchip is still dangerous to other microchips.
# 
# In other words, if a chip is ever left in the same area as another
# RTG, and it's not connected to its own RTG, the chip will be
# fried. Therefore, it is assumed that you will follow procedure and
# keep chips connected to their corresponding RTG when they're in the
# same room, and away from other RTGs otherwise.
# 
# These microchips sound very interesting and useful to your current
# activities, and you'd like to try to retrieve them. The fourth floor
# of the facility has an assembling machine which can make a
# self-contained, shielded computer for you to take with you - that is,
# if you can bring it all of the RTGs and microchips.
# 
# Within the radiation-shielded part of the facility (in which it's safe
# to have these pre-assembly RTGs), there is an elevator that can move
# between the four floors. Its capacity rating means it can carry at
# most yourself and two RTGs or microchips in any combination. (They're
# rigged to some heavy diagnostic equipment - the assembling machine
# will detach it for you.) As a security measure, the elevator will only
# function if it contains at least one RTG or microchip. The elevator
# always stops on each floor to recharge, and this takes long enough
# that the items within it and the items on that floor can irradiate
# each other. (You can prevent this if a Microchip and its Generator end
# up on the same floor in this way, as they can be connected while the
# elevator is recharging.)
# 
# You make some notes of the locations of each component of interest
# (your puzzle input). Before you don a hazmat suit and start moving
# things around, you'd like to have an idea of what you need to do.
# 
# When you enter the containment area, you and the elevator will start on the first floor.
# 
# For example, suppose the isolated area has the following arrangement:
# 
# The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
# The second floor contains a hydrogen generator.
# The third floor contains a lithium generator.
# The fourth floor contains nothing relevant.
# 
# As a diagram (F# for a Floor number, E for Elevator, H for Hydrogen, L
# for Lithium, M for Microchip, and G for Generator), the initial state
# looks like this:
# 
# F4 .  .  .  .  .  
# F3 .  .  .  LG .  
# F2 .  HG .  .  .  
# F1 E  .  HM .  LM 
# 
# Then, to get everything up to the assembling machine on the fourth
# floor, the following steps could be taken:
# 
#     Bring the Hydrogen-compatible Microchip to the second floor, which
#     is safe because it can get power from the Hydrogen Generator:
# 
#     F4 .  .  .  .  .  
#     F3 .  .  .  LG .  
#     F2 E  HG HM .  .  
#     F1 .  .  .  .  LM 
# 
#     Bring both Hydrogen-related items to the third floor, which is
#     safe because the Hydrogen-compatible microchip is getting power
#     from its generator:
# 
#     F4 .  .  .  .  .  
#     F3 E  HG HM LG .  
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  LM 
# 
#     Leave the Hydrogen Generator on floor three, but bring the
#     Hydrogen-compatible Microchip back down with you so you can still
#     use the elevator:
# 
#     F4 .  .  .  .  .  
#     F3 .  HG .  LG .  
#     F2 E  .  HM .  .  
#     F1 .  .  .  .  LM 
# 
#     At the first floor, grab the Lithium-compatible Microchip, which
#     is safe because Microchips don't affect each other:
# 
#     F4 .  .  .  .  .  
#     F3 .  HG .  LG .  
#     F2 .  .  .  .  .  
#     F1 E  .  HM .  LM 
# 
#     Bring both Microchips up one floor, where there is nothing to fry them:
# 
#     F4 .  .  .  .  .  
#     F3 .  HG .  LG .  
#     F2 E  .  HM .  LM 
#     F1 .  .  .  .  .  
# 
#     Bring both Microchips up again to floor three, where they can be
#     temporarily connected to their corresponding generators while the
#     elevator recharges, preventing either of them from being fried:
# 
#     F4 .  .  .  .  .  
#     F3 E  HG HM LG LM 
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  .  
# 
#     Bring both Microchips to the fourth floor:
# 
#     F4 E  .  HM .  LM 
#     F3 .  HG .  LG .  
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  .  
# 
#     Leave the Lithium-compatible microchip on the fourth floor, but
#     bring the Hydrogen-compatible one so you can still use the
#     elevator; this is safe because although the Lithium Generator is
#     on the destination floor, you can connect Hydrogen-compatible
#     microchip to the Hydrogen Generator there:
# 
#     F4 .  .  .  .  LM 
#     F3 E  HG HM LG .  
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  .  
# 
#     Bring both Generators up to the fourth floor, which is safe
#     because you can connect the Lithium-compatible Microchip to the
#     Lithium Generator upon arrival:
# 
#     F4 E  HG .  LG LM 
#     F3 .  .  HM .  .  
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  .  
# 
#     Bring the Lithium Microchip with you to the third floor so you can
#     use the elevator:
# 
#     F4 .  HG .  LG .  
#     F3 E  .  HM .  LM 
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  .  
# 
#     Bring both Microchips to the fourth floor:
# 
#     F4 E  HG HM LG LM 
#     F3 .  .  .  .  .  
#     F2 .  .  .  .  .  
#     F1 .  .  .  .  .  
# 
# In this arrangement, it takes 11 steps to collect all of the objects
# at the fourth floor for assembly. (Each elevator stop counts as one
# step, even if nothing is added to or removed from it.)
# 
# In your situation, what is the minimum number of steps required to
# bring all of the objects to the fourth floor?
#
# --- Part Two ---
# 
# You step into the cleanroom separating the lobby from the isolated
# area and put on the hazmat suit.
# 
# Upon entering the isolated containment area, however, you notice some
# extra parts on the first floor that weren't listed on the record
# outside:
# 
#     An elerium generator.
#     An elerium-compatible microchip.
#     A dilithium generator.
#     A dilithium-compatible microchip.
# 
# These work just like the other generators and microchips. You'll have
# to get them up to assembly as well.

def mk_floor(items):
    """
    Builds a floor from a list of components (generators and microchips)
    """
    return tuple(sorted(items))

def is_empty(floor):
    return len(floor) == 0

def nb_item(floor):
    return len(floor)

def has_generator(floor):
    if len(floor) > 0:
        return floor[-1] > 0
    else:
        return False

def is_valid_floor(floor):
    if has_generator(floor):
        # In other words, if a chip is ever left in the same area as another
        # RTG, and it's not connected to its own RTG, the chip will be fried.
        return all((-chip in floor) for chip in floor if chip < 0)
    else:
        return True


def compute_elevators(floor):
    """
    Computes a list of possible elevators from the content of a floor
    """
    # Elevator takes every combination of 1 to 2 generator/microchip
    #
    # Its capacity rating means it can carry at most yourself and two
    # RTGs or microchips in any combination.
    return list(combinations(floor, 2)) + list(combinations(floor, 1))

def is_valid(elevator, floor):
    """
    Determines if the elevator is compatible with the floor
    """
    # The elevator always stops on each floor to recharge, and this
    # takes long enough that the items within it and the items on that
    # floor can irradiate each other.

    # Creation of a temporary floor
    temp_floor = mk_floor(floor + elevator)

    return is_valid_floor(temp_floor)

def compute_next_states(state):
    """
    Computes the valid possible next states following a given state
    """
    floor_i, floors = state

    next_states = []

    possible_elevators = compute_elevators(floors[floor_i])

    # Build next state (if possible)
    # Each elevator stop counts as one step, even if nothing is added to or removed from it.
    for elevator in possible_elevators:
        # Computation of directions of the elevator
        # Going up
        d_up = (floor_i + 1)
        # Going down
        d_down = (floor_i - 1)
        directions = [d_up, d_down]

        for i in directions:
            if i >= 0 and i < 4:
                if is_valid(elevator, floors[i]):
                    # Updating floor content
                    new_floors = list(floors)
                    # Removing items from the floor
                    new_floors[floor_i] = mk_floor([item for item in floors[floor_i] if item not in elevator])
                    # Adding them to the new floor
                    new_floors[i] = mk_floor(floors[i] + elevator)
                    # Creating the new following state
                    new_state = (i, tuple(new_floors))
                    next_states.append(new_state)

    return next_states

def is_final(state):
    """
    Determines if the floor is final (every components are on the top floor) or not
    """
    floor_i, floors = state
    return (floor_i == 3) and all(is_empty(floor) for floor in floors[:-1])

def print_state(state):
    floor_i, floors = state

    result = 'isFinal: {}\n'.format(is_final(state))
    for i in range(3, -1, -1):
        if floor_i == i:
            floor = '*'
        else:
            floor = ''
        result += '{}\t{}\t{}\t{}\n'.format(floor, is_empty(floors[i]), i, floors[i])
    print(result)



# From: http://www.redblobgames.com/pathfinding/a-star/implementation.html
#
# PriorityQueue for the A* algorithm
class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]

def resolves(initial_state):
    """
    Resolution via A*
    """
    min_path_length = None

    # Mapping:
    # state -> cost
    costs = {initial_state : 0 }

    # Paths to explore
    current_paths = PriorityQueue()
    current_paths.put(initial_state, 0)

    # Early exit flag
    found_final_state = False

    while not current_paths.empty() and not found_final_state:
        current_state = current_paths.get()

        next_states = compute_next_states(current_state)

        for next_state in next_states:
            # Computing new cost (number of steps)
            new_cost = costs[current_state] + 1
            
            # Here, filtering of non-efficient 'next_state'
            if (next_state not in costs) or new_cost < costs[next_state]:
                if is_final(next_state):
                    found_final_state = True # triggering early exit

                    # Updating minimum path length
                    if min_path_length is None:
                        min_path_length = new_cost
                    else:
                        if new_cost < min_path_length:
                            min_path_length = new_cost
                else:
                    costs[next_state] = new_cost
                    # Computing priority
                    i, floors = next_state
                    number_of_items_at_top_floor = nb_item(floors[3])

                    # HERE: heuristics (to adapt given your input)
                    #
                    # The lower the priority, the better the solution is
                    # 
                    priority = new_cost - number_of_items_at_top_floor * 5

                    # Putting in the frontier
                    current_paths.put(next_state, priority)

    return min_path_length

def main():
    # Test input
    #
    # Manual declaration of elements (generators and microchips)
    #
    # Idea of this structure from:
    # https://www.reddit.com/r/adventofcode/comments/5hoia9/2016_day_11_solutions/db1zbu0/
    #
    thulium, strontium = 1, 2
    #
    # Negative elements are: microchips (e.g., -thulium)
    # Positive elements are: generators (e.g, strontium)
    #
    s0 = (0, (
        mk_floor([-thulium, -strontium]), 
        mk_floor([strontium]), 
        mk_floor([thulium]),
        mk_floor([])
    ))
    print('Test input')
    print('Initial state:')
    print_state(s0)
    print('######')

    min_path_length = resolves(s0)
    print('Min path length: {}'.format(min_path_length))
    print('')

    # Part 1
    thulium, plutonium, strontium, promethium, ruthenium, elerium, dilithium = 1, 2, 3, 4, 5, 6, 7
    s0 = (0, (
        mk_floor([-thulium, thulium, plutonium, strontium]), 
        mk_floor([-plutonium, -strontium]), 
        mk_floor([promethium, -promethium, ruthenium, -ruthenium]),
        mk_floor([])
    ))
    print('Part 1')
    print('Initial state:')
    print_state(s0)
    print('######')

    min_path_length = resolves(s0)
    print('Min path length: {}'.format(min_path_length))
    print('')

    # Part 2
    thulium, plutonium, strontium, promethium, ruthenium, elerium, dilithium = 1, 2, 3, 4, 5, 6, 7
    s0 = (0, (
        mk_floor([-thulium, thulium, plutonium, strontium, elerium, -elerium, dilithium, -dilithium]), 
        mk_floor([-plutonium, -strontium]), 
        mk_floor([promethium, -promethium, ruthenium, -ruthenium]),
        mk_floor([])
    ))
    print('Part 2')
    print('Initial state:')
    print_state(s0)
    print('######')

    min_path_length = resolves(s0)
    print('Min path length: {}'.format(min_path_length))

main()
