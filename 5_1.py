
import hashlib

import lib.utils as utils

# Common modulo p and base g.
p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

def main(args):
    # Private numbers.
    a = utils.crypto_random(16)
    b = utils.crypto_random(16)

    print "private keys: a = {}; b = {}".format(a, b)

    A = pow(g, a, p)
    B = pow(g, b, p)
    print "Public keys:\n\tA = {}\n\tB = {}".format(A, B)

    s_a = pow(B, a, p)
    s_b = pow(A, b, p)
    assert s_a == s_b
    print "s is {}".format(s_a)

    sha256 = hashlib.sha256()
    sha256.update(hex(s_a)[:2])
    session_key = sha256.digest()
    print "Session key is {}".format(repr(session_key))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Implement Diffie-Hellman - Challenge 33 (Set 5) of Matasano Crypto Challenge.')
    args = parser.parse_args()

    main(args)
