import io
import re
from itertools import permutations

# --- Day 21: Scrambled Letters and Hash ---
# 
# The computer system you're breaking into uses a weird scrambling
# function to store its passwords. It shouldn't be much trouble to
# create your own scrambled password so you can add it to the system;
# you just have to implement the scrambler.
# 
# The scrambling function is a series of operations (the exact list is
# provided in your puzzle input). Starting with the password to be
# scrambled, apply each operation in succession to the string. The
# individual operations behave as follows:
# 
#     swap position X with position Y means that the letters at indexes
#     X and Y (counting from 0) should be swapped.
#
#     swap letter X with letter Y means that the letters X and Y should
#     be swapped (regardless of where they appear in the string).
#
#     rotate left/right X steps means that the whole string should be
#     rotated; for example, one right rotation would turn abcd into
#     dabc.
#
#     rotate based on position of letter X means that the whole string
#     should be rotated to the right based on the index of letter X
#     (counting from 0) as determined before this instruction does any
#     rotations. Once the index is determined, rotate the string to the
#     right one time, plus a number of times equal to that index, plus
#     one additional time if the index was at least 4.
#
#     reverse positions X through Y means that the span of letters at
#     indexes X through Y (including the letters at X and Y) should be
#     reversed in order.
#
#     move position X to position Y means that the letter which is at
#     index X should be removed from the string, then inserted such that
#     it ends up at index Y.
# 
# For example, suppose you start with abcde and perform the following
# operations:
# 
#     swap position 4 with position 0 swaps the first and last letters,
#     producing the input for the next step, ebcda.
#
#     swap letter d with letter b swaps the positions of d and b: edcba.
#
#     reverse positions 0 through 4 causes the entire string to be
#     reversed, producing abcde.
#
#     rotate left 1 step shifts all letters left one position, causing
#     the first letter to wrap to the end of the string: bcdea.
#
#     move position 1 to position 4 removes the letter at position 1
#     (c), then inserts it at position 4 (the end of the string): bdeac.
#
#     move position 3 to position 0 removes the letter at position 3
#     (a), then inserts it at position 0 (the front of the string):
#     abdec.
#
#     rotate based on position of letter b finds the index of letter b
#     (1), then rotates the string right once plus a number of times
#     equal to that index (2): ecabd.
#
#     rotate based on position of letter d finds the index of letter d
#     (4), then rotates the string right once, plus a number of times
#     equal to that index, plus an additional time because the index was
#     at least 4, for a total of 6 right rotations: decab.
# 
# After these steps, the resulting scrambled password is decab.
# 
# Now, you just need to generate a new scrambled password and you can
# access the system. Given the list of scrambling operations in your
# puzzle input, what is the result of scrambling abcdefgh?

def swap_position(s, pos1, pos2):
    result = ''
    for i, c in enumerate(s):
        if i == pos1:
            result += s[pos2]
        elif i == pos2:
            result += s[pos1]
        else:
            result += c
    
    return result

def swap_letter(s, c1, c2):
    return s.replace(c1, '_') \
            .replace(c2, c1) \
            .replace('_', c2)

LEFT = 'left'
RIGHT = 'right'
def rotate_LR(s, way, n):
    # #First solution:
    #
    # result = ''
    # for i in range(len(s)):
    #     if way == LEFT:
    #         pos = (n + i) % len(s)
    #     else:
    #         pos = (i - n) % len(s)
    #     result += s[pos]

    # return result
    
    n = n % len(s)
    if way == LEFT:
        return s[n:] + s[:n]
    else:
        return s[-n:] + s[:-n]

def rotate_position(s, letter):
    pos = s.index(letter)
    
    if pos >= 4:
        rotation = 2 + pos
    else:
        rotation = 1 + pos
    
    return rotate_LR(s, RIGHT, rotation)

def reverse(s, pos1, pos2):
    reverse = s[pos1:pos2+1][::-1]
    return s[:pos1] + reverse + s[pos2+1:]

def move(s, pos1, pos2):
    result = ''
    j = 0
    for i in range(len(s)):
        if i == pos2: # recopy s[pos1]
            result += s[pos1]
        else:
            if j == pos1: # pass the next j
                j+= 1
            result += s[j]
            j += 1

    return result

pattern_swap_position = re.compile('swap position ([0-9]+) with position ([0-9]+)')
pattern_swap_letter = re.compile('swap letter ([a-zA-Z]) with letter ([a-zA-Z])')
pattern_rotate_left_right = re.compile('rotate (left|right) ([0-9]+) step')
pattern_rotate_position = re.compile('rotate based on position of letter ([a-zA-Z])')
pattern_reverse = re.compile('reverse positions ([0-9]+) through ([0-9]+)')
pattern_move = re.compile('move position ([0-9]+) to position ([0-9]+)')

def apply(operation, s):
    match = pattern_swap_position.match(operation)
    if match is not None:
        pos1 = int(match.group(1))
        pos2 = int(match.group(2))
        return swap_position(s, pos1, pos2)
    else:
        match = pattern_swap_letter.match(operation)
        if match is not None:
            c1 = match.group(1)
            c2 = match.group(2)
            return swap_letter(s, c1, c2)
        else:
            match = pattern_rotate_left_right.match(operation)
            if match is not None:
                way = match.group(1)
                steps = int(match.group(2))
                return rotate_LR(s, way, steps)
            else:
                match = pattern_rotate_position.match(operation)
                if match is not None:
                    letter = match.group(1)
                    return rotate_position(s, letter)
                else:
                    match = pattern_reverse.match(operation)
                    if match is not None:
                        pos1 = int(match.group(1))
                        pos2 = int(match.group(2))
                        return reverse(s, pos1, pos2)
                    else:
                        match = pattern_move.match(operation)
                        if match is not None:
                            pos1 = int(match.group(1))
                            pos2 = int(match.group(2))
                            return move(s, pos1, pos2)
                        else:
                            print('Unable to process: {}'.format(operation))

def scramble(operations, s):
    for operation in operations:
        s = apply(operation, s)

    return s


with io.open('inputs/day21.txt', 'r') as f:
    start = 'abcdefgh'
    operations = [line.strip() for line in f]
    s = scramble(operations, start)
    print('Scrambling {} gives: {}'.format(start, s))

# --- Part Two ---
#
# You scrambled the password correctly, but you discover that you can't
# actually modify the password file on the system. You'll need to
# un-scramble one of the existing passwords by reversing the scrambling
# process.
#
# What is the un-scrambled version of the scrambled password fbgdceah?

def unscramble(operations, s):
    result = None
    perms = [''.join(p) for p in permutations(s)]
    for perm in perms:
        if scramble(operations, perm) == s:
            result = perm
            break

    return result

with io.open('inputs/day21.txt', 'r') as f:
    start = 'fbgdceah'
    operations = [line.strip() for line in f]
    s = unscramble(operations, start)
    print('Unscrambling {} gives: {}'.format(start, s))
