from __future__ import print_function # print utilities without systematic '\n' at EOL
import io
import re

# --- Day 8: Two-Factor Authentication ---
#
# You come across a door implementing what you can only assume is an
# implementation of two-factor authentication after a long game of
# requirements telephone.
#
# To get past the door, you first swipe a keycard (no problem; there was
# one on a nearby desk). Then, it displays a code on a little screen,
# and you type that code on a keypad. Then, presumably, the door
# unlocks.
#
# Unfortunately, the screen has been smashed. After a few minutes,
# you've taken everything apart and figured out how it works. Now you
# just have to work out what the screen would have displayed.
# 
# The magnetic strip on the card you swiped encodes a series of
# instructions for the screen; these instructions are your puzzle
# input. The screen is 50 pixels wide and 6 pixels tall, all of which
# start off, and is capable of three somewhat peculiar operations:
#
#    rect AxB turns on all of the pixels in a rectangle at the top-left of the screen which is A wide and B tall.
#
#    rotate row y=A by B shifts all of the pixels in row A (0 is the top
#    row) right by B pixels. Pixels that would fall off the right end
#    appear at the left end of the row.
#
#    rotate column x=A by B shifts all of the pixels in column A (0 is
#    the left column) down by B pixels. Pixels that would fall off the
#    bottom appear at the top of the column.
#
# For example, here is a simple sequence on a smaller screen:
#
#    rect 3x2 creates a small rectangle in the top-left corner:
#
#   ###....
#   ###....
#   .......
#
#   rotate column x=1 by 1 rotates the second column down by one pixel:
#
#   #.#....
#   ###....
#   .#.....
#
#   rotate row y=0 by 4 rotates the top row right by four pixels:
#
#   ....#.#
#   ###....
#   .#.....
#
#   rotate column x=1 by 1 again rotates the second column down by one
#   pixel, causing the bottom pixel to wrap back to the top:
#
#   .#..#.#
#   #.#....
#   .#.....
#
# As you can see, this display technology is extremely powerful, and
# will soon dominate the tiny-code-displaying-screen market. That's what
# the advertisement on the back of the display tries to convince you,
# anyway.
# 
# There seems to be an intermediate check of the voltage used by the
# display: after you swipe your card, if the screen did work, how many
# pixels should be lit?
#

# --- Part Two ---
#
# You notice that the screen is only capable of displaying capital
# letters; in the font it uses, each letter is 5 pixels wide and 6 tall.
#
# After you swipe your card, what code is the screen trying to display?

pattern_rect = re.compile('rect ([0-9]+)x([0-9]+)')
pattern_rotate_row = re.compile('rotate row y=([0-9]+) by ([0-9]+)')
pattern_rotate_column = re.compile('rotate column x=([0-9]+) by ([0-9]+)')

# Light statuses
ON = '#'
OFF = '.'

# beware of this initialisation!
# -> every cell should be a different string
SCREEN_WIDTH = 50
SCREEN_HEIGHT = 6
SCREEN = [[OFF for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

def print_screen():
    for line in SCREEN:
        for col in line:
            print(col, end='')
        print()
def switch(light_status):
    if light_status == ON:
        return OFF
    else:
        return ON
def nb_ON():
    """
    Computes the number of 'ON' lights in SCREEN
    """
    count = 0
    for i in range(SCREEN_HEIGHT):
        for j in range(SCREEN_WIDTH):
            if SCREEN[i][j] == ON:
                count += 1

    return count

def apply_command(command_line):
    """
    Apply a given command line on SCREEN
    """
    global SCREEN
    rect = pattern_rect.match(command_line)
    if rect is not None:
        # RECT command
        width = int(rect.group(1))
        height = int(rect.group(2))
        for i in range(height):
            for j in range(width):
                SCREEN[i][j] = switch(SCREEN[i][j])

    else:
        # ROTATE ROW command
        rotate_row = pattern_rotate_row.match(command_line)
        if rotate_row is not None:
            y = int(rotate_row.group(1))
            by = int(rotate_row.group(2))

            new_line = [OFF for _ in range(SCREEN_WIDTH)]
            for j in range(SCREEN_WIDTH):
                next_j = (j+by) % SCREEN_WIDTH
                new_line[next_j] = SCREEN[y][j]

            for j,light in enumerate(new_line):
                SCREEN[y][j] = light
        else:
            # ROTATE COLUMN command
            rotate_column = pattern_rotate_column.match(command_line)
            if rotate_column is not None:
                x = int(rotate_column.group(1))
                by = int(rotate_column.group(2))

                new_column = [OFF for _ in range(SCREEN_HEIGHT)]
                for i in range(SCREEN_HEIGHT):
                    next_i = (i+by) % SCREEN_HEIGHT
                    new_column[next_i] = SCREEN[i][x]

                for i,light in enumerate(new_column):
                    SCREEN[i][x] = light

            else:
                print('Unable to match command')

with io.open('inputs/day08.txt', 'r') as f:
    for line in f:
        command = line.strip()
        apply_command(command)

    print_screen()
    print('Number of pixels lit: {}'.format(nb_ON()))
