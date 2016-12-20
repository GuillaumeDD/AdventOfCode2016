import io

# --- Day 20: Firewall Rules ---
# 
# You'd like to set up a small hidden computer here so you can use it to
# get back into the network later. However, the corporate firewall only
# allows communication with certain external IP addresses.
# 
# You've retrieved the list of blocked IPs from the firewall, but the
# list seems to be messy and poorly maintained, and it's not clear which
# IPs are allowed. Also, rather than being written in dot-decimal
# notation, they are written as plain 32-bit integers, which can have
# any value from 0 through 4294967295, inclusive.
# 
# For example, suppose only the values 0 through 9 were valid, and that
# you retrieved the following blacklist:
# 
# 5-8
# 0-2
# 4-7
# 
# The blacklist specifies ranges of IPs (inclusive of both the start and
# end value) that are not allowed. Then, the only IPs that this firewall
# allows are 3 and 9, since those are the only numbers not in any range.
# 
# Given the list of blocked IPs you retrieved from the firewall (your
# puzzle input), what is the lowest-valued IP that is not blocked?

with io.open('inputs/day20.txt', 'r') as f:
    blocked_ranges = []

    def not_in_ranges(v):
        """
        Determines if the value v is not in any ranges (True) or is
        in at least one range (False)
        
        It returns a pair (boolean 'not in range', end of the range in which
        v is contained)
        """
        in_range = True
        found_end = None
        for start, end in blocked_ranges:
            if v >= start and v <= end:
                in_range = False
                found_end = end
                break
        return (in_range, found_end)

    # Loading of ranges
    for line in f:
        content = line.split('-')
        first = int(content[0])
        second = int(content[1])
        blocked_ranges.append((first, second))
    
    # Searching IP
    found_IP = False
    ip = 0
    while not found_IP and ip <= 4294967295:
        (not_in_range, found_end) = not_in_ranges(ip)
        if not_in_range:
            found_IP = True
        else:
            ip = found_end + 1
    
    print('The lowest-valued IP that is not blocked is: {}'.format(ip))

    # --- Part Two ---
    # 
    # How many IPs are allowed by the blacklist?
    #

    # Sorting the ranges by 'start' in pairs (start, end)
    blocked_ranges = sorted(blocked_ranges)
    
    start, end = blocked_ranges[0]
    nb_blocked_ip = 0
    for r in blocked_ranges:
        if r[0] > (end + 1): # this range does not overlap with previous one
            nb_blocked_ip += end - start + 1
            start, end = r
        else: # this range overlaps with the previous one
            end = max(r[1], end)

    # Taking into account last range
    nb_blocked_ip += end - start + 1

    nb_allowed_ips = 4294967296 - nb_blocked_ip # beware: 4294967296 = 4294967295 - 0 + 1
    
    print('There are {} IPs allowed by the blacklist.'.format(nb_allowed_ips))
