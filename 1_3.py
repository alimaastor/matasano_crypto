
import argparse

from lib.Message import Message

ciphered_text = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

def main():

    result = []

    for i in xrange(256):
        key = chr(i)
        message = Message().set_hex(ciphered_text).xor(key)
        score = message.score()
        result.append((score, message, key))

    result.sort(reverse=True)

    print "For a score of [{}], key is [{}] and message is [{}]".format(*result[0])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Single-byte XOR cipher - Challenge 3 (Set 1) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()
