import io

# --- Day 3: Squares With Three Sides ---
#
# Now that you can think clearly, you move deeper into the labyrinth of
# hallways and office furniture that makes up this part of Easter Bunny
# HQ. This must be a graphic design department; the walls are covered in
# specifications for triangles.
#
# Or are they?
#
# The design document gives the side lengths of each triangle it
# describes, but... 5 10 25? Some of these aren't triangles. You can't
# help but mark the impossible ones.
#
# In a valid triangle, the sum of any two sides must be larger than the
# remaining side. For example, the "triangle" given above is impossible,
# because 5 + 10 is not larger than 25.
#
# In your puzzle input, how many of the listed triangles are possible?
#

def is_possible_triangle(side_lengths):
    return (side_lengths[0] + side_lengths[1]) > side_lengths[2] and \
           (side_lengths[0] + side_lengths[2]) > side_lengths[1] and \
           (side_lengths[1] + side_lengths[2]) > side_lengths[0]

with io.open('inputs/day03.txt') as f:
    counter = 0
    for line in f:
        triangle = [int(length) for length in line.split(' ') if length.strip() != '']
        if is_possible_triangle(triangle):
            counter += 1
    print('Number of possible triangles: {}'.format(counter))

# --- Part Two ---
#
# Now that you've helpfully marked up their design documents, it occurs
# to you that triangles are specified in groups of three
# vertically. Each set of three numbers in a column specifies a
# triangle. Rows are unrelated.
#
# For example, given the following specification, numbers with the same
# hundreds digit would be part of the same triangle:
#
# 101 301 501
# 102 302 502
# 103 303 503
# 201 401 601
# 202 402 602
# 203 403 603
#
# In your puzzle input, and instead reading by columns, how many of the
# listed triangles are possible?
#
with io.open('inputs/day03.txt') as f:
    line_i = 1
    triangles = [] # accumulator for the triangles

    triangle_A = [] # triangle in the column 1
    triangle_B = [] # triangle in the column 2
    triangle_C = [] # triangle in the column 3

    # Reading triangles from the file
    for line in f:
        # Reading line
        lengths = [int(length) for length in line.split(' ') if length.strip() != '']
        # Appending the lengths to the adequate triangles
        triangle_A.append(lengths[0])
        triangle_B.append(lengths[1])
        triangle_C.append(lengths[2])

        # Saving triangles and resetting if needed
        if line_i % 3 == 0:
            triangles.append(triangle_A)
            triangles.append(triangle_B)
            triangles.append(triangle_C)

            triangle_A = []
            triangle_B = []
            triangle_C = []

        line_i += 1

    # Computation of valid triangles
    counter = 0
    for triangle in triangles:
        if is_possible_triangle(triangle):
            counter += 1

    print('Number of possible triangles: {}'.format(counter))        
