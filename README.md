# Description #
This project provides solutions to the [Advent of Code 2016](http://adventofcode.com).

# Installation #
Solutions can be ran  from Python 2.7. Inputs of the  problems are in the
'inputs' directory.

For instance :

	$ python day01.py

# Notes about the Provided Solutions #
1. Day 1: No Time for a Taxicab
1. Day 2: Bathroom Security
1. Day 3: Squares With Three Sides
1. Day 4: Security Through Obscurity
1. Day 5: How About a Nice Game of Chess?
   + Usage of hashlib and hexdigest
1. Day 6: Signals and Noise
   + Usage of collections.Counter
1. Day 7: Internet Protocol Version 7
   + Usage of re to split a string given more than one delimiter
   + Implementation of 'slice_n' for a string (generator of substring of
     size 'n')
1. Day 8: Two-Factor Authentication
1. Day 9: Explosives in Cyberspace
   + Regular expression (via re)
   + Recursivity
1. Day 10: Balance Bots
1. Day 11: Radioisotope Thermoelectric Generators
   + Solution is based on A* algorithm (there is a need to tweak the heuristics)
   + Input is manually set in the code
   + Usage of itertools, heapq
   + Usage of immutable datastructure (tuples)
1. Day 12: Leonardo's Monorail
   + Naive solution using regex
   + Takes some time for part 2
1. Day 13: A Maze of Twisty Little Cubicles
   + Solution is based on Dijkstra's algorithm
   + Usage of heapq (PriorityQueue)
1. Day 14: One-Time Pad
   + Usage of hashlib and hexdigest
   + Usage of regex backreferences
   + Caching results of stretch hash for efficiency (part 2)
1. Day 15: Timing is Everything
1. Day 16: Dragon Checksum
1. Day 17: Two Steps Forward
   + First part: breadth-first search (BFS)
1. Day 18: Like a Rogue
1. Day 19: An Elephant Named Joseph
   + Second  part uses  a double-linked  list for  solving this  kind of
     pop/append problem
1. Day 20: Firewall Rules
1. Day 21: Scrambled Letters and Hash
   + Usage of permutations from itertools for part 2 (brute-forcing)
1. Day 22: Grid Computing
   + Part 2 is resolved manually by displaying the grid
1. Day 23: Safe Cracking
   + Reusing solution of day 12
   + Part 2 is solved by hacking the interpreter between line 4 and 10
1. Day 24: Air Duct Spelunking
   + Reusing implementation of day 13 (Dijkstra's algorithm)
1. Day 25: Clock Signal
   + Adapting solutions of day 12 and 23
   +  Solutions is  found by  brute-forcing and  checking the  first 100
     generated items
   
# License #
GPLv3 - see the COPYING file.

