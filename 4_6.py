
from lib.MD4 import MD4
import lib.utils as utils

def main():
    passwd = utils.get_passwd()
    message = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    to_digest = passwd + message

    d = MD4()
    d.update(to_digest)
    correct_digest = d.digest()
    print "Correct digest:", correct_digest

    d2 = MD4(*MD4.get_state_from_hex_str(correct_digest))
    d2.update(";admin=true")
    print "Modified digest:", d2.digest()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Break an MD4 keyed MAC using length extension - Challenge 30 (Set 4) of Matasano Crypto Challenge.')

    main()
