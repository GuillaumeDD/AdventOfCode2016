import io
import re

# --- Day 12: Leonardo's Monorail ---
# 
# You finally reach the top floor of this building: a garden with a
# slanted glass ceiling. Looks like there are no more stars to be had.
# 
# While sitting on a nearby bench amidst some tiger lilies, you manage
# to decrypt some of the files you extracted from the servers
# downstairs.
# 
# According to these documents, Easter Bunny HQ isn't just this building
# - it's a collection of buildings in the nearby area. They're all
# connected by a local monorail, and there's another building not far
# from here! Unfortunately, being night, the monorail is currently not
# operating.
# 
# You remotely connect to the monorail control systems and discover that
# the boot sequence expects a password. The password-checking logic
# (your puzzle input) is easy to extract, but the code it uses is
# strange: it's assembunny code designed for the new computer you just
# assembled. You'll have to execute the code and get the password.
# 
# The assembunny code you've extracted operates on four registers (a, b,
# c, and d) that start at 0 and can hold any integer. However, it seems
# to make use of only a few instructions:
# 
#     cpy x y copies x (either an integer or the value of a register) into register y.
#
#     inc x increases the value of register x by one.
#
#     dec x decreases the value of register x by one.
#
#     jnz x y jumps to an instruction y away (positive means forward;
#     negative means backward), but only if x is not zero.
# 
# The jnz instruction moves relative to itself: an offset of -1 would
# continue at the previous instruction, while an offset of 2 would skip
# over the next instruction.
# 
# For example:
# 
# cpy 41 a
# inc a
# inc a
# dec a
# jnz a 2
# dec a
# 
# The above code would set register a to 41, increase its value by 2,
# decrease its value by 1, and then skip the last dec a (because a is
# not zero, so the jnz a 2 skips it), leaving register a at 42. When you
# move past the last instruction, the program halts.
# 
# After executing the assembunny code in your puzzle input, what value
# is left in register a?

pattern_cpy = re.compile('cpy ([-0-9]+|a|b|c|d) (a|b|c|d)')
pattern_inc = re.compile('inc (a|b|c|d)')
pattern_dec = re.compile('dec (a|b|c|d)')
pattern_jnz = re.compile('jnz ([-0-9]+|a|b|c|d) ([-0-9]+)')

def execute(registers, instructions):
    i = 0
    while i >= 0 and i < len(instructions):
        instruction = instructions[i]

        # CPY
        match = pattern_cpy.match(instruction)
        if match is not None:
            x = match.group(1)
            y = match.group(2)
            
            if x.isdigit():
                x = int(x)
                registers[y] = x
            else:
                registers[y] = registers[x]
            i += 1

        # INC
        match = pattern_inc.match(instruction)
        if match is not None:
            x = match.group(1)
            registers[x] += 1
            i += 1

        # DEC
        match = pattern_dec.match(instruction)
        if match is not None:
            x = match.group(1)
            registers[x] -= 1
            i += 1

        # JNZ
        match = pattern_jnz.match(instruction)
        if match is not None:
            x = match.group(1)
            if x.isdigit():
                x_value = int(x)
            else:
                x_value = registers[x]

            shift = int(match.group(2))

            if x_value != 0:
                i += shift
            else:
                i += 1
        
    print(registers)    

with io.open('inputs/day12.txt', 'r') as f:
    registers = {
        'a' : 0,
        'b' : 0,
        'c' : 0,
        'd' : 0
    }
    
    instructions = [line.strip() for line in f]
    print('Part 1')
    execute(registers, instructions)

# --- Part Two ---
# 
# As you head down the fire escape to the monorail, you notice it didn't
# start; register c needs to be initialized to the position of the
# ignition key.
# 
# If you instead initialize register c to be 1, what value is now left
# in register a?
#
with io.open('inputs/day12.txt', 'r') as f:
    registers = {
        'a' : 0,
        'b' : 0,
        'c' : 1, # part 2 special
        'd' : 0
    }
    
    instructions = [line.strip() for line in f]
    print('Part 2')
    execute(registers, instructions)
