
import hashlib
from Crypto.Cipher import AES

import lib.utils as utils
from lib.Message import Message

def get_cypher():
 AES.new(get_passwd(), AES.MODE_CBC, IV=get_passwd())

# Common modulo p and base g.
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

message_a = 'This is A\'s message'
message_b = 'Other message which happens to be B\'s message'

a = utils.crypto_random(16)
b = utils.crypto_random(16)

def negotiate(p, g, title):
    print "******************"
    print title
    print "******************"
    print ""

    A = pow(g, a, p)
    print "A is {}".format(A)

    # A->B: Send "p", "g"
    print "A->B: Send \"p\", \"g\""

    # B->M->A: Send ACK
    B = pow(g, b, p)
    print "B is {}".format(B)
    print "B->A: Send ACK"

    # A->M->B: Send "A"
    print "A->B: Send \"A\""
    s_b = pow(A, b, p)
    print "S for B is {}".format(repr(s_b))

    # B->M->A: Send "B"
    print "B->A: Send \"B\""
    s_a = pow(B, a, p)
    print "S for A is {}".format(repr(s_a))
    print "================="
    print "================="
    print ""

def main(args):
    print "p is {}".format(p)
    print "g is {}".format(g)
    print ""
    print "a is {}".format(a)
    print "b is {}".format(b)
    print ""

    # g = 1
    negotiate(p, 1, title='g = 1')
    # g = p
    negotiate(p, p, title='g = p')
    # g = p - 1
    negotiate(p, p - 1, title='g = p - 1')

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=(
            'Implement DH with negotiated groups, and break with malicious "g" parameters'
            ' - Challenge 35 (Set 5) of Matasano Crypto Challenge.'))
    args = parser.parse_args()

    main(args)
