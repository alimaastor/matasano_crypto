
import argparse
import random
from collections import OrderedDict

from lib.utils import Cypher
from lib.Message import Message

def parse_structured_cookie(string):
    result = {}
    for pair in string.split('&'):
        key, value = pair.split('=')
        result[key] = value
    return result

def profile_for(string):
    r = OrderedDict()
    r['email'] = string.translate(None, '&=')
    r['uid']   = 15
    r['role']  = 'user'
    return '&'.join(map(lambda x: '{}={}'.format(*x), r.iteritems()))

def main():
    cypher = Cypher()

    user_profile = profile_for('aaa@gmail.com')
    encrypted_profile = cypher.encrypt(user_profile)
    print "Encrypted text is [{}]".format(repr(encrypted_profile))

    false_profile = profile_for('aaaaaaaaaa' + Message('root').padding().to_str())
    encrypted_false_profile = cypher.encrypt(false_profile)
    interesting_bit = encrypted_false_profile[16:32]

    print "Decrypted false profile is [{}]".format(cypher.decrypt(encrypted_profile[:-16] + interesting_bit)[:-12])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='ECB cut-and-paste - Challenge 13 (Set 2) of Matasano Crypto Challenge.')

    args = parser.parse_args()

    main()
