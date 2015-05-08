
import argparse

from lib.Message import Message

def main(message):
    print Message(message).padding(block_length=20)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Implement PKCS#7 padding - Challenge 9 (Set 2) of Matasano Crypto Challenge.')
    parser.add_argument('message',
        help='Message to be padded.', type=str)

    args = parser.parse_args()

    main(args.message)
