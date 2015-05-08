
import argparse

from lib.Message import Message

def main(message, key):
	print repr(Message(message).xor(key).to_str())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Implement repeating-key XOR - Challenge 5 (Set 1) of Matasano Crypto Challenge.')
    parser.add_argument('message',
        help='Message to be ciphered.', type=str)
    parser.add_argument('key',
        help='Key to use to cipher message.', type=str)

    args = parser.parse_args()

    main(args.message, args.key)
