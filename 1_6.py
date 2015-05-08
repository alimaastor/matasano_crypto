
import argparse
import os

from lib.Message import Message
from itertools import product

def get_input_string(path_to_file):
    string = ''
    with open(path_to_file, 'r') as f:
        for line in f:
            string += line.replace('\n', '')
    return string

def main():
    # Get ciphered message.
    ciphered_message = Message().set_b64(
        get_input_string(os.path.join("data", "1_6_data.txt"))
    )

    # Value initialization.
    best_score = -float('inf')
    best_password = ''
    best_deciphered_text = ''

    results = []
    iteration = 0

    keysize = ciphered_message.get_block_sizes(1)[0]
    blocks_chars = []

    n_blocks = len(ciphered_message)/keysize

    for block in zip(*[ciphered_message[i:i+keysize] for i in xrange(0, keysize * n_blocks, keysize)]):
        iteration += 1
        block = ''.join(block)
        assert len(block) == n_blocks
        block_chars = []
        for char in xrange(256):
            ciphered_block = Message(block).xor(chr(char))
            score = ciphered_block.score()
            block_chars.append((score, chr(char), ciphered_block))
        block_chars.sort(reverse=True)
        blocks_chars.append([ch for sc, ch, msg in block_chars[:1]])

    for password in product(*blocks_chars):
        assert len(password) == keysize
        password = ''.join(password)
        message = Message(ciphered_message).xor(password)
        score = message.score()
        results.append((score, message, password))

    results.sort(reverse=True)

    print "Keysize:", keysize, "\n"
    print 'Message:\n', message, "\n"
    print 'Password:', password, "\n"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Break repeating-key XOR - Challenge 6 (Set 1) of Matasano Crypto Challenge.')
    args = parser.parse_args()

    main()
