
import hashlib

from lib.SHA1 import SHA1
from lib.Message import Message

def main(text):
    sha1 = SHA1()
    sha1.update(text)
    m = sha1.hexdigest()
    print m

    d = hashlib.sha1()
    d.update(text)
    assert d.hexdigest() == m

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Implement a SHA-1 keyed MAC - Challenge 28 (Set 4) of Matasano Crypto Challenge.')

    parser.add_argument('text',
        help='Text to digest', type=str, nargs='?', default='aaaaaaaaaaaaaaaa')

    args = parser.parse_args()

    main(args.text)
