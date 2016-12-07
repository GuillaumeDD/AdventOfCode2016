import io
import re

# --- Day 7: Internet Protocol Version 7 ---
#
# While snooping around the local network of EBHQ, you compile a list of
# IP addresses (they're IPv7, of course; IPv6 is much too
# limited). You'd like to figure out which IPs support TLS
# (transport-layer snooping).
#
# An IP supports TLS if it has an Autonomous Bridge Bypass Annotation,
# or ABBA. An ABBA is any four-character sequence which consists of a
# pair of two different characters followed by the reverse of that pair,
# such as xyyx or abba. However, the IP also must not have an ABBA
# within any hypernet sequences, which are contained by square brackets.
# 
# For example:
#
#    abba[mnop]qrst supports TLS (abba outside square brackets).
#
#    abcd[bddb]xyyx does not support TLS (bddb is within square
#    brackets, even though xyyx is outside square brackets).
#
#    aaaa[qwer]tyui does not support TLS (aaaa is invalid; the interior
#    characters must be different).
#
#    ioxxoj[asdfgh]zxcvbn supports TLS (oxxo is outside square brackets,
#    even though it's within a larger string).
#
# How many IPs in your puzzle input support TLS?
#

def slice_n(s, n):
    """
    Generator of slices of size 'n' from a given string 's'

    if n > len(s) it returns an empty generator
    """
    assert n > 0, 'Slice must be strictly superior to 0'
    
    number_of_slices = max(0, len(s) - n + 1)

    for i in range(number_of_slices):
        yield s[i:i+n]

def is_palindrome(str4char):
    """
    Determines whether the given 4-character sequence is
    a palindrome with 2 different characters or not.
    """
    assert len(str4char) == 4, 'len({}) != 4'.format(str4char)

    return str4char[0] != str4char[1] and \
           str4char[0] == str4char[3] and \
           str4char[1] == str4char[2]

def support_TLS(ipv7):
    """
    Determines whether a given IPv7 IP supports TLS (transport-layer
    snooping)
    """
    # Splitting supernet and hypernet sequences
    # Pair indexes correspond to supernet sequences
    # Impair indexes correspond to hypernet sequences
    tokens = re.split('[\[\]]', ipv7)

    support_TLS = False
    continue_exploration = True
    i = 0
    while i < len(tokens) and continue_exploration:
        if i % 2 == 0: # outside [...]: supernet sequences
            for subtoken in slice_n(tokens[i], 4):
                if is_palindrome(subtoken):
                    support_TLS = True
        else: # inside [ ... ]: the hypernet sequence
            # the IP also must not have an ABBA within any hypernet sequences
            for subtoken in slice_n(tokens[i], 4):
                if is_palindrome(subtoken):
                    support_TLS = False
                    continue_exploration = False
                    break
        i += 1
    
    return support_TLS

with io.open('inputs/day07.txt') as f:
    nb_ip = 0
    for line in f:
        ip = line.strip()
        if support_TLS(ip):
            nb_ip += 1

    print('Number of IPs supporting TLS: {}'.format(nb_ip))


# --- Part Two ---
#
# You would also like to know which IPs support SSL (super-secret
# listening).
#
# An IP supports SSL if it has an Area-Broadcast Accessor, or ABA,
# anywhere in the supernet sequences (outside any square bracketed
# sections), and a corresponding Byte Allocation Block, or BAB, anywhere
# in the hypernet sequences. An ABA is any three-character sequence
# which consists of the same character twice with a different character
# between them, such as xyx or aba. A corresponding BAB is the same
# characters but in reversed positions: yxy and bab, respectively.
#
# For example:
#
#    aba[bab]xyz supports SSL (aba outside square brackets with
#    corresponding bab within square brackets).
#
#    xyx[xyx]xyx does not support SSL (xyx, but no corresponding yxy).
#
#    aaa[kek]eke supports SSL (eke in supernet with corresponding kek in
#    hypernet; the aaa sequence is not related, because the interior
#    character must be different).
#
#    zazbz[bzb]cdb supports SSL (zaz has no corresponding aza, but zbz
#    has a corresponding bzb, even though zaz and zbz overlap).
#
# How many IPs in your puzzle input support SSL?
#
def is_ABA(str3char):
    """
    Determines whether the given 3-character sequence is
    of the form ABA (with A!=B)
    """
    assert len(str3char) == 3, 'len({}) != 3'.format(str3char)

    return str3char[0] != str3char[1] and \
           str3char[0] == str3char[2]

def match_ABA_BAB(aba, bab):
    """
    Determines if the characters a and b in aba are the same that
    characters a and b in bab
    """
    assert len(aba) == 3, 'len({}) != 3'.format(aba)
    assert len(bab) == 3, 'len({}) != 3'.format(bab)

    return aba[0] == bab[1] and \
           aba[1] == bab[0] and \
           aba[1] == bab[2]

def support_SSL(ipv7):
    """
    Determines whether a given IPv7 IP supports SSL (super-secret listening)
    """    
    # Splitting supernet and hypernet sequences
    # Pair indexes correspond to supernet sequences
    # Impair indexes correspond to hypernet sequences
    tokens = re.split('[\[\]]', ipv7)

    support_SSL = False

    abas = set()
    def contains_matching_ABA(bab): # helper for set 'abas'
        result = False
        for aba in abas:
            if match_ABA_BAB(aba, bab):
                result = True
                break

        return result

    babs = set()
    def contains_matching_BAB(aba): # helper for set 'babs'
        result = False
        for bab in babs:
            if match_ABA_BAB(aba, bab):
                result = True
                break

        return result

    i = 0
    while i < len(tokens) and not support_SSL:
        if i % 2 == 0: # outside [...]: supernet sequences
            for subtoken in slice_n(tokens[i], 3):
                if is_ABA(subtoken) and not support_SSL:
                    abas.add(subtoken)
                    support_SSL = contains_matching_BAB(subtoken)

        else: # inside [ ... ]: the hypernet sequence
            for subtoken in slice_n(tokens[i], 3):
                if is_ABA(subtoken) and not support_SSL:
                    babs.add(subtoken)
                    support_SSL = contains_matching_ABA(subtoken)
        i += 1
    
    return support_SSL

with io.open('inputs/day07.txt') as f:
    nb_ip = 0
    for line in f:
        ip = line.strip()

        if support_SSL(ip):
            nb_ip += 1

    print('Number of IPs supporting SSL: {}'.format(nb_ip))
