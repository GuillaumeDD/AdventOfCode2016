import io
import re

# --- Day 25: Clock Signal ---
# 
# You open the door and find yourself on the roof. The city sprawls away
# from you for miles and miles.
# 
# There's not much time now - it's already Christmas, but you're nowhere
# near the North Pole, much too far to deliver these stars to the sleigh
# in time.
# 
# However, maybe the huge antenna up here can offer a solution. After
# all, the sleigh doesn't need the stars, exactly; it needs the timing
# data they provide, and you happen to have a massive signal generator
# right here.
# 
# You connect the stars you have to your prototype computer, connect
# that to the antenna, and begin the transmission.
# 
# Nothing happens.
# 
# You call the service number printed on the side of the antenna and
# quickly explain the situation. "I'm not sure what kind of equipment
# you have connected over there," he says, "but you need a clock
# signal." You try to explain that this is a signal for a clock.
# 
# "No, no, a clock signal - timing information so the antenna computer
# knows how to read the data you're sending it. An endless, alternating
# pattern of 0, 1, 0, 1, 0, 1, 0, 1, 0, 1...." He trails off.
# 
# You ask if the antenna can handle a clock signal at the frequency you
# would need to use for the data from the stars. "There's no way it can!
# The only antenna we've installed capable of that is on top of a
# top-secret Easter Bunny installation, and you're definitely not-" You
# hang up the phone.
# 
# You've extracted the antenna's clock signal generation assembunny code
# (your puzzle input); it looks mostly compatible with code you worked
# on just recently.
# 
# This antenna code, being a signal generator, uses one extra instruction:
# 
#     out x transmits x (either an integer or the value of a register)
#     as the next value for the clock signal.
# 
# The code takes a value (via register a) that describes the signal to
# generate, but you're not sure how it's used. You'll have to find the
# input to produce the right signal through experimentation.
# 
# What is the lowest positive integer that can be used to initialize
# register a and cause the code to output a clock signal of 0, 1, 0,
# 1... repeating forever?
# 

pattern_cpy = re.compile('cpy ([-0-9]+|a|b|c|d) (a|b|c|d)')
pattern_inc = re.compile('inc (a|b|c|d)')
pattern_dec = re.compile('dec (a|b|c|d)')
pattern_jnz = re.compile('jnz ([-0-9]+|a|b|c|d) ([-0-9]+|a|b|c|d)')

pattern_toggle = re.compile('tgl ([-0-9]+|a|b|c|d)')

pattern_out = re.compile('out ([-0-9]+|a|b|c|d)')

def execute(registers, instructions, steps):
    """
    Execute 'instructions' with the 'registers' to output 'steps' elements
    """
    def val(x):
        if x in registers:
            return registers[x]
        else:
            return int(x)

    output = []
    i = 0
    nb_steps = 0

    while i >= 0 and i < len(instructions) and nb_steps < steps:
        instruction = instructions[i]
        i += 1

        # OUT
        match = pattern_out.match(instruction)
        if match is not None:
            x = match.group(1)
            x_value = val(x)
            
            output.append(x_value)
            nb_steps += 1

        # CPY
        match = pattern_cpy.match(instruction)
        if match is not None:
            x = match.group(1)
            y = match.group(2)
            registers[y] = val(x)

        # INC
        match = pattern_inc.match(instruction)
        if match is not None:
            x = match.group(1)
            registers[x] += 1

        # DEC
        match = pattern_dec.match(instruction)
        if match is not None:
            x = match.group(1)
            registers[x] -= 1

        # JNZ
        match = pattern_jnz.match(instruction)
        if match is not None:
            x = match.group(1)
            x_value = val(x)

            y = match.group(2)
            y_value = val(y)

            shift = y_value

            if x_value != 0:
                i += shift - 1
        
    return output


def check_cycle(l):
    """
    Check if l represents a cycle of 0,1,0,1,... (true) or not (false)
    """
    for i, item in enumerate(l):
        if i % 2 == 0 and item != 0:
            return False
        elif i % 2 == 1 and item != 1:
            return False

    return True

with io.open('inputs/day25.txt', 'r') as f:
    instructions = [line.strip() for line in f]
    print('Trying to generate clock signal...')

    # Solutions is found by brute-forcing from 0 until we find an 'i'
    # that generates a cycle of 0/1 of 'N' elements
    N = 100
    found = False
    i = 0
    while not found:
        print('Trying {}'.format(i))
        registers = {
            'a' : i,
            'b' : 0,
            'c' : 0,
            'd' : 0
        }
        
        output = execute(registers, instructions, N)
        if check_cycle(output):
            print('Found: {}'.format(i))
            found = True
        i += 1
