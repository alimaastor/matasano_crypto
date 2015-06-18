
import argparse
import os
from Crypto.Cipher import AES

from lib.utils import get_passwd
from lib.Message import Message


def edit(ciphertext, key, offset, newtext):
    cypher = AES.new(get_passwd(), AES.MODE_CTR, counter=lambda: "\x00" * 16)
    plaintext = cypher.decrypt(ciphertext)
    for index, newchar in enumerate(newtext):
        plaintext[offset + index] = newchar
    return cypher.encrypt(plaintext)

def main():
    cypher = AES.new(get_passwd(), AES.MODE_CTR, counter=lambda: "\x00" * 16)
    with open(os.path.join('data', '4_1_data.txt'), 'r') as datafile:
        ciphertext = cypher.encrypt(Message().set_b64(datafile.read().replace('\n', '')).to_str())

    assert ciphertext == edit(ciphertext, get_passwd(), 0, '')

    keystream = ''
    for index, cipherchar in enumerate(ciphertext):
        new_ciphertext = edit(ciphertext, get_passwd(), index, 'a')
        keystream += chr(ord(new_ciphertext[index]) ^ ord('a'))

    assert len(keystream) == len(ciphertext)

    print Message(ciphertext).xor(keystream).to_str()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Break "random access read/write" AES CTR - Challenge 25 (Set 4) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()
