import io
import re

# --- Day 10: Balance Bots ---
# 
# You come upon a factory in which many robots are zooming around
# handing small microchips to each other.
# 
# Upon closer examination, you notice that each bot only proceeds when
# it has two microchips, and once it does, it gives each one to a
# different bot or puts it in a marked "output" bin. Sometimes, bots
# take microchips from "input" bins, too.
# 
# Inspecting one of the microchips, it seems like they each contain a
# single number; the bots must use some logic to decide what to do with
# each chip. You access the local control computer and download the
# bots' instructions (your puzzle input).
# 
# Some of the instructions specify that a specific-valued microchip
# should be given to a specific bot; the rest of the instructions
# indicate what a given bot should do with its lower-value or
# higher-value chip.
# 
# For example, consider the following instructions:
# 
# value 5 goes to bot 2
# bot 2 gives low to bot 1 and high to bot 0
# value 3 goes to bot 1
# bot 1 gives low to output 1 and high to bot 0
# bot 0 gives low to output 2 and high to output 0
# value 2 goes to bot 2
# 
#     Initially, bot 1 starts with a value-3 chip, and bot 2 starts with
#     a value-2 chip and a value-5 chip.
#
#     Because bot 2 has two microchips, it gives its lower one (2) to
#     bot 1 and its higher one (5) to bot 0.
#
#     Then, bot 1 has two microchips; it puts the value-2 chip in output
#     1 and gives the value-3 chip to bot 0.
#
#     Finally, bot 0 has two microchips; it puts the 3 in output 2 and
#     the 5 in output 0.
# 
# In the end, output bin 0 contains a value-5 microchip, output bin 1
# contains a value-2 microchip, and output bin 2 contains a value-3
# microchip. In this configuration, bot number 2 is responsible for
# comparing value-5 microchips with value-2 microchips.
# 
# Based on your instructions, what is the number of the bot that is
# responsible for comparing value-61 microchips with value-17
# microchips?


# Patterns to parse input string instructions
subpattern_bot_or_output = '([a-zA-Z0-9 ]+)'

pattern_target = re.compile('(bot|output) ([0-9]+)')

pattern_value = re.compile('value ([0-9]+) goes to {}$'.format(subpattern_bot_or_output))
pattern_gives = re.compile('{0} gives low to {0} and high to {0}'.format(subpattern_bot_or_output))

def _get_target(s):
    """
    From a string representing a target, returns its type and its ID

    For instance, 'bot 42' returns ('bot', 42)
    """
    match = pattern_target.match(s)
    return (match.group(1), int(match.group(2)))

# State of the machine
BOT = 'bot'
OUTPUT = 'output'
bots_and_outputs = {
    BOT: {}, # mapping: ID -> (low value, high value)
    OUTPUT: {}, # mapping: ID -> value
}

def _pop_low_and_high(bot_target):
    """
    Pop low and high value of a bot and returns a pair (low value, high value)
    """
    (target_type, target_id) = bot_target
    assert target_type == BOT, \
           'Try to pop low and high value of a non-bot ({})'.format(target_type)
    (low_value, high_value) = bots_and_outputs[target_type][target_id]

    bots_and_outputs[target_type][target_id] = (None, None)

    return (low_value, high_value)

def _put(target, new_value):
    """
    Puts a new value for a target (bot or output)
    """
    (target_type, target_id) = target

    # First time initialisation
    if target_id not in bots_and_outputs[target_type]:
        if target_type == BOT:
            bots_and_outputs[target_type][target_id] = (None, None)
        else: # case: output
            bots_and_outputs[target_type][target_id] = None

    if target_type == BOT:
        (low_value, high_value) = bots_and_outputs[target_type][target_id]

        assert (low_value is None) or (high_value is None), 'Target {} is full!'.format(target)

        if low_value is None:
            bots_and_outputs[target_type][target_id] = (new_value, None)
        else: # insertion and keeping value ordered
            if low_value > new_value:
                bots_and_outputs[target_type][target_id] = (new_value, low_value)
            else:
                bots_and_outputs[target_type][target_id] = (low_value, new_value)

                # Answer to question
                (low_value, high_value) = bots_and_outputs[target_type][target_id]
                if low_value == 17 and high_value == 61:
                    print('{} {} is responsible for comparing 17 and 61'.format(target_type, target_id))
    else: # case: output
        bots_and_outputs[target_type][target_id] = new_value

def _is_bot_complete(bot_target):
    """
    Determines whether a bot has low and high values (True), or not (False)
    """
    (target_type, target_id) = bot_target
    assert target_type == BOT, \
           'Try to pop low and high value of a non-bot ({})'.format(target_type)

    if target_id not in bots_and_outputs[target_type]:
        return False
    else:
        (low_value, high_value) = bots_and_outputs[target_type][target_id]
        return (low_value is not None) and (high_value is not None)

def _can_take(target):
    """
    Determines whether a target can take an additional value (True), or not
    """
    (target_type, target_id) = target
    if target_type == BOT:
        return not _is_bot_complete(target)
    else: # ouput
        return True

def is_applicable_value(target):
    """
    Determines whether it is possible to apply a 'value' instruction (True)
    or not (False)
    """
    return not _is_bot_complete(target)

def is_applicable_gives(giver, taker_low, taker_high):
    """
    Determines whether it is possible to apply a 'gives' instruction (True)
    or not (False)
    """
    return _is_bot_complete(giver) and \
           _can_take(taker_low) and \
           _can_take(taker_high)

def process_instruction(instruction):
    """
    Process one instruction if possible (return None), or if not
    (return the instruction)
    """
    match = pattern_value.match(instruction)
    if match is not None:
        # Instruction: value
        value = int(match.group(1))
        target = _get_target(match.group(2))
        if is_applicable_value(target):
            _put(target, value)
            outcome = None
        else:
            outcome = instruction
    else:
        match = pattern_gives.match(instruction)
        if match is not None:
            # Instruction: gives
            giver = _get_target(match.group(1))
            taker_low = _get_target(match.group(2))
            taker_high = _get_target(match.group(3))
            
            if is_applicable_gives(giver, taker_low, taker_high):
                low_value, high_value = _pop_low_and_high(giver)

                _put(taker_low, low_value)
                _put(taker_high, high_value)
                outcome = None
            else:
                outcome = instruction
        else:
            print('Unable to process: {}'.format(instruction))
            outcome = instruction

    return outcome

def evaluate_instructions(instructions):
    paused_instructions = []

    while len(instructions) > 0:
        instruction = instructions[0]
        other_instructions = instructions[1:]

        outcome = process_instruction(instruction)

        if outcome is not None:
            # Instruction cannot be processed
            paused_instructions.append(outcome)
            instructions = other_instructions
        else:
            # Instruction has been processed
            # Trying back previous instructions
            paused_instructions.extend(other_instructions)
            instructions = paused_instructions
            paused_instructions = []

# --- Part Two ---
#
# What do you get if you multiply together the values of one chip in
# each of outputs 0, 1, and 2?

def _get_output_value(target_id):
    if target_id not in bots_and_outputs[OUTPUT]:
        return None
    else:
        return bots_and_outputs[OUTPUT][target_id]

def part2():
    low1 = _get_output_value(0)
    low2 = _get_output_value(1)
    low3 = _get_output_value(2)

    if (low1 is not None and low2 is not None and low3 is not None):
        print('Solution to part 2: {}'.format(low1 * low2 * low3))

# Execution of instructions
with io.open('./inputs/day10.txt') as f:
    instructions = f.readlines()
    evaluate_instructions(instructions)
    part2()
