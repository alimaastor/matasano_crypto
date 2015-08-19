
import hashlib

from lib.SHA1 import SHA1
import lib.utils as utils

def main():
    passwd = utils.get_passwd()
    message = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    to_digest = passwd + message

    d = hashlib.sha1()
    d.update(to_digest)
    correct_digest = d.hexdigest()
    print "Correct digest:", correct_digest

    sha1 = SHA1(*SHA1.get_state_from_hex_str(correct_digest))
    sha1.update(";admin=true")
    print "Modified digest:", sha1.hexdigest()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Break a SHA-1 keyed MAC using length extension - Challenge 29 (Set 4) of Matasano Crypto Challenge.')

    main()
