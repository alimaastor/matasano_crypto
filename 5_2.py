
import hashlib
from Crypto.Cipher import AES

import lib.utils as utils
from lib.Message import Message

class NonCompilantAsciiTextException(Exception):
    def __init__(self, text):
        self.text = text


def get_cypher():
 AES.new(get_passwd(), AES.MODE_CBC, IV=get_passwd())

# Common modulo p and base g.
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

def main(args):

    message_a = 'This is A\'s message'
    message_b = 'Other message which happens to be B\'s message'

    print "p is {}".format(p)
    print "g is {}".format(g)

    # A->M: Send "p", "g", "A"
    a = utils.crypto_random(16)
    A = pow(g, a, p)
    print "A->M: Sending p, g and A = {}".format(A)

    # M->B: Send "p", "g", "p"
    print "M->B: Sending p, g and A = p"

    # B->M: Send "B"
    b = utils.crypto_random(16)
    B = pow(g, b, p)
    s_b = pow(p, b, p)
    print "S of B calculated as {}".format(s_b)
    print "B->M: Sending B = {}".format(B)

    # M->A: Send "p"
    print "M->A: Sending p as B".format(p, B)
    s_a = pow(p, a, p)
    print "S of A calculated as {}".format(s_a)

    # A->M: Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
    sha1_a = hashlib.sha1()
    sha1_a.update(Message().set_int(s_a).to_str())
    cypher_a =  AES.new(sha1_a.digest()[:16], AES.MODE_CBC, IV="\x00" * 16)
    ciphered_message_a = cypher_a.encrypt(Message(message_a).padding().to_str())
    print "A->M: Sending AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv = \"{}\"".format(repr(ciphered_message_a))

    # M->B: Relay that to B
    sha1_m = hashlib.sha1()
    sha1_m.update(Message().set_int(0).to_str())
    cypher_m =  AES.new(sha1_m.digest()[:16], AES.MODE_CBC, IV="\x00" * 16)
    print "M->B: pass message on, but we know that message is {}".format(repr(cypher_m.decrypt(ciphered_message_a)))

    # B->M: Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
    sha1_b = hashlib.sha1()
    sha1_b.update(Message().set_int(s_b).to_str())
    cypher_b =  AES.new(sha1_b.digest()[:16], AES.MODE_CBC, IV="\x00" * 16)
    ciphered_message_b = cypher_a.encrypt(Message(message_b).padding().to_str())
    print "B->M: Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv = {}".format(repr(ciphered_message_b))

    # M->A: Relay that to A
    print "M->A: pass message on, but we know that message is {}".format(repr(cypher_m.decrypt(ciphered_message_b)))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description=(
            'Implement a MITM key-fixing attack on Diffie-Hellman with parameter injection'
            ' - Challenge 33 (Set 5) of Matasano Crypto Challenge.'))
    args = parser.parse_args()

    main(args)
