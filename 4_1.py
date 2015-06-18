
import argparse
import os
import base64
from Crypto.Cipher import AES

from lib.utils import get_passwd
from lib.Message import Message


def edit(ciphertext, key, offset, newtext):
    cypher = AES.new(get_passwd(), AES.MODE_CTR, counter=lambda: "\x00" * 16)
    plaintext = cypher.decrypt(ciphertext)
    plaintext = plaintext[:offset] + newtext + plaintext[offset + len(newtext):]
    cypher = AES.new(get_passwd(), AES.MODE_CTR, counter=lambda: "\x00" * 16)
    return cypher.encrypt(plaintext)

def main():
    cypher = AES.new(get_passwd(), AES.MODE_CTR, counter=lambda: "\x00" * 16)
    with open(os.path.join('data', '4_1_data.txt'), 'r') as datafile:
        c = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
        plaintext = c.decrypt(datafile.read().decode('base64'))
        ciphertext = cypher.encrypt(plaintext)

    assert ciphertext == edit(ciphertext, get_passwd(), 0, '')

    keystream = ''
    for index, cipherchar in enumerate(ciphertext):
        new_ciphertext = edit(ciphertext, get_passwd(), index, 'a')
        keystream += chr(ord(new_ciphertext[index]) ^ ord('a'))

    assert len(keystream) == len(ciphertext)

    print Message(ciphertext).xor_whole(keystream).to_str()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Break "random access read/write" AES CTR - Challenge 25 (Set 4) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()
