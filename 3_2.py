
import argparse

from lib.MyAesCtrCypher import MyAesCtrCypher

def main(message, password):
    print "For message [{}] and password [{}]".format(message, password)
    c = MyAesCtrCypher(password)
    print "Encrypted message is [{}]".format(repr(c.encrypt(message)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Implement CTR, the stream cipher mode - Challenge 18 (Set 3) of Matasano Crypto Challenge.')
    parser.add_argument('message',
        help='Message to be encrypted using CTR and then decrypted', type=str)
    parser.add_argument('password',
        help='Password to encrypt messages using CTR and then decrypted', type=str)

    args = parser.parse_args()

    main(args.message, args.password)
