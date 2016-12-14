import io
import hashlib
import re

# --- Day 14: One-Time Pad ---
# 
# In order to communicate securely with Santa while you're on this
# mission, you've been using a one-time pad that you generate using a
# pre-agreed algorithm. Unfortunately, you've run out of keys in your
# one-time pad, and so you need to generate some more.
# 
# To generate keys, you first get a stream of random data by taking the
# MD5 of a pre-arranged salt (your puzzle input) and an increasing
# integer index (starting with 0, and represented in decimal); the
# resulting MD5 hash should be represented as a string of lowercase
# hexadecimal digits.
# 
# However, not all of these MD5 hashes are keys, and you need 64 new
# keys for your one-time pad. A hash is a key only if:
# 
#     It contains three of the same character in a row, like 777. Only
#     consider the first such triplet in a hash.
#
#     One of the next 1000 hashes in the stream contains that same
#     character five times in a row, like 77777.
# 
# Considering future hashes for five-of-a-kind sequences does not cause
# those hashes to be skipped; instead, regardless of whether the current
# hash is a key, always resume testing for keys starting with the very
# next hash.
# 
# For example, if the pre-arranged salt is abc:
# 
#     The first index which produces a triple is 18, because the MD5
#     hash of abc18 contains ...cc38887a5.... However, index 18 does not
#     count as a key for your one-time pad, because none of the next
#     thousand hashes (index 19 through index 1018) contain 88888.
#
#     The next index which produces a triple is 39; the hash of abc39
#     contains eee. It is also the first key: one of the next thousand
#     hashes (the one at index 816) contains eeeee.
#
#     None of the next six triples are keys, but the one after that, at
#     index 92, is: it contains 999 and index 200 contains 99999.
#
#     Eventually, index 22728 meets all of the criteria to generate the 64th key.
# 
# So, using our example salt of abc, index 22728 produces the 64th key.
# 
# Given the actual salt in your puzzle input, what index produces your
# 64th one-time pad key?

def hash(s):
    return hashlib.md5(s).hexdigest()

regex_pattern = re.compile('(?P<char>.)(?P=char)(?P=char)')
def contains_three_character_in_row(h):
    match = regex_pattern.search(h)
    if match is None:
        return None
    else:
        return match.group(1) # the repeated character


def is_compliant_next_thousand(salt, i, c, hashing):
    """
    Determines if the next thousand (from i+1 to i+1000) keys built from 'salt'
    contains 5 times 'c'
    """
    row = c * 5
    hash_found = False
    j = 1
    while j <= 1000 and not hash_found:
        attempt = '{}{}'.format(salt, i + j)
        hex_hash = hashing(attempt)
        
        if row in hex_hash:
            hash_found = True

        j += 1

    return hash_found

def is_key(h, salt, current_i, hashing):
    """
    Determine if a hash is a key
    
    A hash is a key only if:

    - It contains three of the same character in a row, like 777. Only
      consider the first such triplet in a hash
    
    - One of the next 1000 hashes in the stream contains that same
      character five times in a row, like 77777.
    """
    repeated_character = contains_three_character_in_row(h)
    if repeated_character is None:
        return False
    else:
        return is_compliant_next_thousand(salt, current_i, repeated_character, hashing)

def find_keys(salt, n = 64, hashing = hash):
    """
    Find n valid keys

    Returns a mapping key number (starting from 1) to a pair (index, hash)
    """
    i = 0
    count = 0
    keys = {}

    while count < n:
        attempt = '{}{}'.format(salt,i)
        hex_hash = hashing(attempt)
        if is_key(hex_hash, salt, i, hashing):
            count += 1
            keys[count] = (i, hex_hash)
        i += 1

    return keys

with io.open('inputs/day14.txt', 'r') as f:
    salt = f.readlines()[0].strip()
    keys = find_keys(salt)
    (index, key) = keys[64]
    print('Index of the 64th key with salt={}: {}'.format(salt, index))


# --- Part Two ---
# 
# Of course, in order to make this process even more secure, you've also
# implemented key stretching.
# 
# Key stretching forces attackers to spend more time generating
# hashes. Unfortunately, it forces everyone else to spend more time,
# too.
# 
# To implement key stretching, whenever you generate a hash, before you
# use it, you first find the MD5 hash of that hash, then the MD5 hash of
# that hash, and so on, a total of 2016 additional hashings. Always use
# lowercase hexadecimal representations of hashes.
# 
# For example, to find the stretched hash for index 0 and salt abc:
# 
#     Find the MD5 hash of abc0: 577571be4de9dcce85a041ba0410f29f.
#     Then, find the MD5 hash of that hash: eec80a0c92dc8a0777c619d9bb51e910.
#     Then, find the MD5 hash of that hash: 16062ce768787384c81fe17a7a60c7e3.
#     ...repeat many times...
#     Then, find the MD5 hash of that hash: a107ff634856bb300138cac6568c0f24.
# 
# So, the stretched hash for index 0 in this situation is a107ff.... In
# the end, you find the original hash (one use of MD5), then find the
# hash-of-the-previous-hash 2016 times, for a total of 2017 uses of MD5.
# 
# The rest of the process remains the same, but now the keys are
# entirely different. Again for salt abc:
# 
#     The first triple (222, at index 5) has no matching 22222 in the
#     next thousand hashes.
#
#     The second triple (eee, at index 10) hash a matching eeeee at
#     index 89, and so it is the first key.
#
#     Eventually, index 22551 produces the 64th key (triple fff with
#     matching fffff at index 22859.
# 
# Given the actual salt in your puzzle input and using 2016 extra MD5
# calls of key stretching, what index now produces your 64th one-time
# pad key?

_stretch_cache = {}
def stretch(s):
    if s in _stretch_cache:
        return _stretch_cache[s]
    else:
        current_hash = s
        for i in range(2017):
            current_hash = hash(current_hash)
        
        _stretch_cache[s] = current_hash
            
        return current_hash

with io.open('inputs/day14.txt', 'r') as f:
    salt = f.readlines()[0].strip()
    keys = find_keys(salt, hashing = stretch)
    (index, key) = keys[64]
    print('Index of the 64th key with salt={}: {}'.format(salt, index))
