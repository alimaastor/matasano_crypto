
import sys
from lib.Message import Message
from itertools import product

def get_input_string(path_to_file):
    string = ''
    with open(path_to_file, 'r') as f:
        for line in f:
            string += line.replace('\n', '')
    return string

if __name__ == '__main__':
    
    ciphered_message = Message().set_b64(get_input_string(sys.argv[1]))

    best_score = -float('inf')
    best_password = ''
    best_deciphered_text = ''

    results = []
    iteration = 0

    for keysize in ciphered_message.get_block_sizes(1):
        print 'for a key size of', keysize
        blocks_chars = []

        n_blocks = len(ciphered_message)/keysize

        for block in zip(*[ciphered_message[i:i+keysize] for i in xrange(0, keysize * n_blocks, keysize)]):
            iteration += 1
            block = ''.join(block)
            assert len(block) == n_blocks
            block_chars = []
            for char in xrange(256):
                ciphered_block = Message(block).cipher(chr(char))
                score = ciphered_block.score()
                block_chars.append((score, chr(char), ciphered_block))
                # print (score, chr(char), ciphered_block)
                # raw_input()
            block_chars.sort(reverse=True)
            blocks_chars.append([ch for sc, ch, msg in block_chars[:1]])

        for password in product(*blocks_chars):
            assert len(password) == keysize
            password = ''.join(password)
            message = Message(ciphered_message).cipher(password)
            score = message.score()
            results.append((score, message, password))

    results.sort(reverse=True)
    
    print 'Message:\n', message
    print 'Password:', password
