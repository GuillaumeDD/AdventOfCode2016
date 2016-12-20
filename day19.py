import io

# --- Day 19: An Elephant Named Joseph ---
# 
# The Elves contact you over a highly secure emergency channel. Back at
# the North Pole, the Elves are busy misunderstanding White Elephant
# parties.
# 
# Each Elf brings a present. They all sit in a circle, numbered starting
# with position 1. Then, starting with the first Elf, they take turns
# stealing all the presents from the Elf to their left. An Elf with no
# presents is removed from the circle and does not take turns.
# 
# For example, with five Elves (numbered 1 to 5):
# 
#   1
# 5   2
#  4 3
# 
#     Elf 1 takes Elf 2's present.
#     Elf 2 has no presents and is skipped.
#     Elf 3 takes Elf 4's present.
#     Elf 4 has no presents and is also skipped.
#     Elf 5 takes Elf 1's two presents.
#     Neither Elf 1 nor Elf 2 have any presents, so both are skipped.
#     Elf 3 takes Elf 5's three presents.
# 
# So, with five Elves, the Elf that sits starting in position 3 gets all
# the presents.
# 
# With the number of Elves given in your puzzle input, which Elf gets
# all the presents?

def resolves(n):
    # Datastructure:
    # - index: 0 1 2 3 4
    # - elves: 1 2 3 4 5
    elves = tuple(i for i in range(1, n + 1))
    
    while len(elves) != 1:
        if len(elves) % 2 == 1: 
            elves = tuple(k for index, k in enumerate(elves) if index % 2 == 0 and index != 0)
        else:
            elves = tuple(k for index, k in enumerate(elves) if index % 2 == 0)

    return elves[0]

with io.open('inputs/day19.txt', 'r') as f:
    INPUT = int(f.readlines()[0])

elf_id = resolves(INPUT)
print('The Elf getting all the presents is Elf {}.'.format(elf_id))

# -- Part Two ---
# 
# Realizing the folly of their present-exchange rules, the Elves agree
# to instead steal presents from the Elf directly across the circle. If
# two Elves are across the circle, the one on the left (from the
# perspective of the stealer) is stolen from. The other rules remain
# unchanged: Elves with no presents are removed from the circle
# entirely, and the other elves move in slightly to keep the circle
# evenly spaced.
# 
# For example, with five Elves (again numbered 1 to 5):
# 
#     The Elves sit in a circle; Elf 1 goes first:
# 
#       1
#     5   2
#      4 3
# 
#     Elves 3 and 4 are across the circle; Elf 3's present is stolen,
#     being the one to the left. Elf 3 leaves the circle, and the rest
#     of the Elves move in:
# 
#       1           1
#     5   2  -->  5   2
#      4 -          4
# 
#     Elf 2 steals from the Elf directly across the circle, Elf 5:
# 
#       1         1 
#     -   2  -->     2
#       4         4 
# 
#     Next is Elf 4 who, choosing between Elves 1 and 2, steals from Elf 1:
# 
#      -          2  
#         2  -->
#      4          4
# 
#     Finally, Elf 2 steals from Elf 4:
# 
#      2
#         -->  2  
#      -
# 
# So, with five Elves, the Elf that sits starting in position 2 gets all the presents.
# 
# With the number of Elves given in your puzzle input, which Elf now
# gets all the presents?

# Double linked-list
class Elf:
    def __init__(self, elf_id):
        self.id = elf_id
        self.next_elf = None
        self.previous_elf = None
    
    def delete(self):
        self.previous_elf.next_elf = self.next_elf
        self.next_elf.previous_elf = self.previous_elf

def resolves(n):
    # Initialisation of elves
    elves = {}
    for i in range(n):
        elves[i] = Elf(i + 1)
    # Linking the elves
    for i in range(n):
        elves[i].next_elf = elves[(i+1) % n]
        elves[i].previous_elf = elves[(i-1) % n]
    
    start = elves[0]
    middle = elves[n/2]

    for i in range(n-1):
        middle.delete()
        start = start.next_elf
        
        number_of_elves = n - i
        middle = middle.next_elf
        if number_of_elves % 2 == 1:
            middle = middle.next_elf

    return start.id

elf_id = resolves(INPUT)
print('The Elf getting all the presents is Elf {}.'.format(elf_id))
