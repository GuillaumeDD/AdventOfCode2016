import io
import re

# --- Day 4: Security Through Obscurity ---
#
# Finally, you come across an information kiosk with a list of rooms. Of
# course, the list is encrypted and full of decoy data, but the
# instructions to decode the list are barely hidden nearby. Better
# remove the decoy data first.
#
# Each room consists of an encrypted name (lowercase letters separated
# by dashes) followed by a dash, a sector ID, and a checksum in square
# brackets.
#
# A room is real (not a decoy) if the checksum is the five most common
# letters in the encrypted name, in order, with ties broken by
# alphabetization. For example:
#
#     aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common
#     letters are a (5), b (3), and then a tie between x, y, and z,
#     which are listed alphabetically.
#
#     a-b-c-d-e-f-g-h-987[abcde] is a real room because although the
#     letters are all tied (1 of each), the first five are listed
#     alphabetically.
#
#     not-a-real-room-404[oarel] is a real room.
#
#     totally-real-room-200[decoy] is not.
#
# Of the real rooms from the list above, the sum of their sector IDs is
# 1514.
#
# What is the sum of the sector IDs of the real rooms?
#

def line_to_room(line):
    """
    From a line representing a room, returns a triple:
    (encrypted room name, sector ID, checksum)

    E.g., for the line: 'aaaaa-bbb-z-y-x-123[abxyz]' it returns:
    ('aaaaa-bbb-z-y-x', 123, 'abxyz')
    """
    pattern = re.compile("([a-z\-]+)([0-9]+)\[([a-z]+)\]")

    match = pattern.match(line)

    encrypted_name = match.group(1)[:-1] # removes the last '-'
    sector_id = int(match.group(2))
    checksum = match.group(3)

    return (encrypted_name, sector_id, checksum)

def is_valid_checksum(room_name, checksum):
    """
    Returns True if 'checksum' is valid for 'room_name', else False
    """
    distribution = {}
    
    # Computation of the character distribution
    for c in room_name:
        if c != '-':
            if c in distribution:
                distribution[c] += 1
            else:
                distribution[c] = 1
    
    # Computation of the checksum
    last_freq = -1
    checksum_size = 5
    computed_checksum = ''
    
    def compare(a, b):
        """
        Helper comparison function to order by descending frequence and then by
        ascending character value
        """
        (c1, freq1) = a
        (c2, freq2) = b
        if freq1 == freq2:
            if c1 < c2:
                return -1
            elif c1 > c2:
                return 1
            else:
                return 0
        else:
            return freq2 - freq1

    five_commonest_items = [c for (c, freq) in sorted(distribution.items(), cmp=compare)[:5]]
    computed_checksum = ''.join(five_commonest_items)

    return computed_checksum == checksum

with io.open('inputs/day04.txt', 'r') as f:
    sum_of_real_rooms = 0

    for line in f:
        (encrypted_name, sector_id, checksum) = line_to_room(line.strip())

        if is_valid_checksum(encrypted_name, checksum):
            sum_of_real_rooms += sector_id

    print('Sum of the sector IDs of the real rooms: {}'.format(sum_of_real_rooms))

#--- Part Two ---
#
# With all the decoy data out of the way, it's time to decrypt this list
# and get moving.
#
# The room names are encrypted by a state-of-the-art shift cipher, which
# is nearly unbreakable without the right software. However, the
# information kiosk designers at Easter Bunny HQ were not expecting to
# deal with a master cryptographer like yourself.
#
# To decrypt a room name, rotate each letter forward through the
# alphabet a number of times equal to the room's sector ID. A becomes B,
# B becomes C, Z becomes A, and so on. Dashes become spaces.
#
# For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.
#
# What is the sector ID of the room where North Pole objects are stored?
#

def decipher(letter, shift):
    """
    Move a letter between 'a' and 'z' by a given shift
    """
    #     |<------length------>|
    #     a                    z
    # ----+---------------+----+
    #                     ^
    #                   letter
    #     |<-letter_pos-->|
    #     
    length = ord('z') - ord('a') + 1
    letter_pos = ord(letter) - ord('a')

    new_letter_code = ord('a') + (letter_pos + shift) % length

    return chr(new_letter_code)

def decipher_name(encrypted_name, sector_id):
    """
    Decipher a room name

    '-' are turned into ' '
    """
    deciphered_name = ''
    for c in encrypted_name:
        if c == '-':
            deciphered_name += ' '
        else:
            deciphered_name += decipher(c, sector_id)

    return deciphered_name

with io.open('inputs/day04.txt', 'r') as f:
    for line in f:
        (encrypted_name, sector_id, checksum) = line_to_room(line.strip())
        if is_valid_checksum(encrypted_name, checksum):
            uncrypted_name = decipher_name(encrypted_name, sector_id)
            if 'north' in uncrypted_name:
                print('Room name: {}; sector ID: {}; checksum: {}'.format(uncrypted_name, sector_id, checksum))
