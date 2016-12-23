import io
import re

# --- Day 23: Safe Cracking ---
# 
# This is one of the top floors of the nicest tower in EBHQ. The Easter
# Bunny's private office is here, complete with a safe hidden behind a
# painting, and who wouldn't hide a star in a safe behind a painting?
# 
# The safe has a digital screen and keypad for code entry. A sticky note
# attached to the safe has a password hint on it: "eggs". The painting
# is of a large rabbit coloring some eggs. You see 7.
# 
# When you go to type the code, though, nothing appears on the display;
# instead, the keypad comes apart in your hands, apparently having been
# smashed. Behind it is some kind of socket - one that matches a
# connector in your prototype computer! You pull apart the smashed
# keypad and extract the logic circuit, plug it into your computer, and
# plug your computer into the safe.
# 
# Now, you just need to figure out what output the keypad would have
# sent to the safe. You extract the assembunny code from the logic chip
# (your puzzle input).
# 
# The code looks like it uses almost the same architecture and
# instruction set that the monorail computer used! You should be able to
# use the same assembunny interpreter for this as you did there, but
# with one new instruction:
# 
# tgl x toggles the instruction x away (pointing at instructions like
# jnz does: positive means forward; negative means backward):
# 
#     For one-argument instructions, inc becomes dec, and all other
#     one-argument instructions become inc.
#
#     For two-argument instructions, jnz becomes cpy, and all other
#     two-instructions become jnz.
#
#     The arguments of a toggled instruction are not affected.
#
#     If an attempt is made to toggle an instruction outside the
#     program, nothing happens.
#
#     If toggling produces an invalid instruction (like cpy 1 2) and an
#     attempt is later made to execute that instruction, skip it
#     instead.
#
#     If tgl toggles itself (for example, if a is 0, tgl a would target
#     itself and become inc a), the resulting instruction is not
#     executed until the next time it is reached.
# 
# For example, given this program:
# 
# cpy 2 a
# tgl a
# tgl a
# tgl a
# cpy 1 a
# dec a
# dec a
# 
#     cpy 2 a initializes register a to 2.
#
#     The first tgl a toggles an instruction a (2) away from it, which
#     changes the third tgl a into inc a.
#
#     The second tgl a also modifies an instruction 2 away from it,
#     which changes the cpy 1 a into jnz 1 a.
#
#     The fourth line, which is now inc a, increments a to 3.
#
#     Finally, the fifth line, which is now jnz 1 a, jumps a (3)
#     instructions ahead, skipping the dec a instructions.
# 
# In this example, the final value in register a is 3.
# 
# The rest of the electronics seem to place the keypad entry (the number
# of eggs, 7) in register a, run the code, and then send the value left
# in register a to the safe.
# 
# What value should be sent to the safe?
# 

pattern_cpy = re.compile('cpy ([-0-9]+|a|b|c|d) (a|b|c|d)')
pattern_inc = re.compile('inc (a|b|c|d)')
pattern_dec = re.compile('dec (a|b|c|d)')
pattern_jnz = re.compile('jnz ([-0-9]+|a|b|c|d) ([-0-9]+|a|b|c|d)')

pattern_toggle = re.compile('tgl ([-0-9]+|a|b|c|d)')

def execute(registers, instructions):
    i = 0
    while i >= 0 and i < len(instructions):
        instruction = instructions[i]

        # TGL
        match = pattern_toggle.match(instruction)
        if match is not None:
            x = match.group(1)
            if x.isdigit():
                x_value = int(x)
            else:
                x_value = registers[x]
            
            i_to_toggle = i + x_value
            if i_to_toggle < len(instructions): # If an attempt is made
                                                # to toggle an
                                                # instruction outside
                                                # the program, nothing
                                                # happens.
                instruction_to_tgl = instructions[i_to_toggle]
                if 'inc' in instruction_to_tgl:
                    # inc become dec
                    instructions[i_to_toggle] = instruction_to_tgl.replace('inc', 'dec')
                elif 'dec' in instruction_to_tgl:
                    # all other one-argument instructions become inc
                    instructions[i_to_toggle] = instruction_to_tgl.replace('dec', 'inc')
                elif 'tgl' in instruction_to_tgl:
                    instructions[i_to_toggle] = instruction_to_tgl.replace('tgl', 'inc')
                elif 'jnz' in instruction_to_tgl:
                    # jnz becomes cpy
                    instructions[i_to_toggle] = instruction_to_tgl.replace('jnz', 'cpy')
                elif 'cpy' in instruction_to_tgl:
                    # all other two-instructions become jnz
                    instructions[i_to_toggle] = instruction_to_tgl.replace('cpy', 'jnz')
            i += 1

        # CPY
        match = pattern_cpy.match(instruction)
        if match is not None:
            x = match.group(1)
            y = match.group(2)

            try:
                 x = int(x)
                 registers[y] = x
            except:
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
            
            try:
                x_value = int(x)
            except:
                x_value = registers[x]

            y = match.group(2)
            try:
                y_value = int(y)
            except:
                y_value = registers[y]

            shift = y_value

            if x_value != 0:
                i += shift
            else:
                i += 1
        


    print(registers)    

with io.open('inputs/day23.txt', 'r') as f:
    registers = {
        'a' : 7,
        'b' : 0,
        'c' : 0,
        'd' : 0
    }
    
    instructions = [line.strip() for line in f]
    print('Part 1')
    execute(registers, instructions)

# --- Part Two ---
# 
# The safe doesn't open, but it does make several angry noises to
# express its frustration.
# 
# You're quite sure your logic is working correctly, so the only other
# thing is... you check the painting again. As it turns out, colored
# eggs are still eggs. Now you count 12.
# 
# As you run the program with this new input, the prototype computer
# begins to overheat. You wonder what's taking so long, and whether the
# lack of any instruction more powerful than "add one" has anything to
# do with it. Don't bunnies usually multiply?
# 
# Anyway, what value should actually be sent to the safe?

def execute(registers, instructions):
    i = 0
    while i >= 0 and i < len(instructions):
        instruction = instructions[i]

        # HACKING THE CODE TO MULTIPLY
        # cpy b c
        # inc a
        # dec c
        # jnz c -2
        # dec d
        # jnz d -5
        if i == 4:
            registers['a'] = registers['b']*registers['d']
            registers['c'] = 0
            registers['d'] = 0
            i = 10
            continue
        
        # TGL
        match = pattern_toggle.match(instruction)
        if match is not None:
            x = match.group(1)
            if x.isdigit():
                x_value = int(x)
            else:
                x_value = registers[x]
            
            i_to_toggle = i + x_value
            if i_to_toggle < len(instructions): # If an attempt is made
                                                # to toggle an
                                                # instruction outside
                                                # the program, nothing
                                                # happens.
                instruction_to_tgl = instructions[i_to_toggle]
                if 'inc' in instruction_to_tgl:
                    # inc become dec
                    instructions[i_to_toggle] = instruction_to_tgl.replace('inc', 'dec')
                elif 'dec' in instruction_to_tgl:
                    # all other one-argument instructions become inc
                    instructions[i_to_toggle] = instruction_to_tgl.replace('dec', 'inc')
                elif 'tgl' in instruction_to_tgl:
                    instructions[i_to_toggle] = instruction_to_tgl.replace('tgl', 'inc')
                elif 'jnz' in instruction_to_tgl:
                    # jnz becomes cpy
                    instructions[i_to_toggle] = instruction_to_tgl.replace('jnz', 'cpy')
                elif 'cpy' in instruction_to_tgl:
                    # all other two-instructions become jnz
                    instructions[i_to_toggle] = instruction_to_tgl.replace('cpy', 'jnz')
            i += 1

        # CPY
        match = pattern_cpy.match(instruction)
        if match is not None:
            x = match.group(1)
            y = match.group(2)

            try:
                 x = int(x)
                 registers[y] = x
            except:
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
            
            try:
                x_value = int(x)
            except:
                x_value = registers[x]

            y = match.group(2)
            try:
                y_value = int(y)
            except:
                y_value = registers[y]

            shift = y_value

            if x_value != 0:
                i += shift
            else:
                i += 1
        


    print(registers)    


with io.open('inputs/day23.txt', 'r') as f:
    registers = {
        'a' : 12,
        'b' : 0,
        'c' : 0,
        'd' : 0
    }
    
    instructions = [line.strip() for line in f]
    print('Part 2')
    execute(registers, instructions)
