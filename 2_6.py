
import sys
import random
import json
from Crypto.Cipher import AES

from lib.Message import Message
from lib.Cypher import Cypher
from lib.utils import get_random_length_text

def create_lookup_table(cypher, substring, block_size):
    lookup_table = {}
    for c in xrange(256):
        element = substring + chr(c)
        assert len(element) == block_size
        lookup_table[cypher.encrypt(element)] = element
    return lookup_table

if __name__ == '__main__':

    message = Message().set_b64(''.join((
        'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg',
        'aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq',
        'dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg',
        'YnkK')))

    cypher = Cypher()

    # Detect block size of the cypher.
    for i in xrange(1,129):
        m = Message(cypher.encrypt(2 * i * 'a'))
        if m[:i] == m[i:2*i]:
            block_size = i
            break

    print 'block size is', block_size, 'using ECB mode.\n'

    decrypted_message = ''
    char_index = 0
    while True:
    # for char_index in xrange(len(message)):

        block_no, subblock_index = divmod(char_index, block_size)

        prefix = (block_size - subblock_index - 1) * 'a'

        if block_no:
            lookup_string_value = decrypted_message[1 - block_size:]
        else:
            lookup_string_value = prefix + decrypted_message[:subblock_index]

        lookup_table = create_lookup_table(cypher, lookup_string_value, block_size)

        encrypted = cypher.encrypt(get_random_length_text() + prefix + message.to_str())

        try:
            next_char = lookup_table[encrypted[16 + block_no * block_size : 16 + (block_no + 1) * block_size]][-1]
        except KeyError:
            continue
        else:
            decrypted_message += next_char
            char_index += 1
            if len(decrypted_message) == len(message):
                break

    assert decrypted_message == message.to_str()
    print 'Text is:\n', decrypted_message
