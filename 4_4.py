
import hashlib

from lib.sha1 import sha1
from lib.Message import Message

def main(text):
    m = Message().set_hex(sha1(text))
    print repr(m.to_str())

    d = hashlib.sha1()
    d.update(text)
    assert repr(d.digest()) == repr(m.to_str())

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Implement a SHA-1 keyed MAC - Challenge 28 (Set 4) of Matasano Crypto Challenge.')

    parser.add_argument('text',
        help='Text to digest', type=str, nargs='?', default='aaaaaaaaaaaaaaaa')

    args = parser.parse_args()

    main(args.text)
