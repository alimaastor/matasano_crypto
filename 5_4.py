
import hashlib
import hmac

from lib.Message import Message
from lib.utils import crypto_random

def main(args):
    # C & S: Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    N = 0x009f4f57c0d386b90c5cf147d96466c5c7b2d154e7d32a58695191847f58f5e2ca9c28b497ae1b31d1c2507b1c489662a9d39c5b5100503888cfd7c762a7c1310d26b8ae38ad8de4ba3ff800022221c73be2da3113b4a7ba404a32a446adb9dedb2958bab3b26f2984396e1af1fc28594182b2a72de7fed99ea03e34c0d69e02db
    g = 2
    k = 3
    I = 'example@mail.com'
    P = 'somepassword1234'
    print "C & S: Agree on N={}, g={}, k={}, I ({}), P ({})".format(
        N, g, k, I, P)
    print ""

    # S:
    print "S:"

    #   Generate salt as random integer
    salt = crypto_random(32)
    salt_str = Message().set_int(salt).to_str()
    print "  Generate salt as random integer:", salt

    #   Generate string xH=SHA256(salt|password)
    #   Convert xH to integer x somehow (put 0x on hexdigest)
    x_sha256_generator = hashlib.sha256()
    x_sha256_generator.update(salt_str + P)
    x = int(x_sha256_generator.hexdigest(), 16)
    print "  Generate string xH=SHA256(salt|password)"
    print "  Convert xH to integer x somehow (put 0x on hexdigest):", x

    #   Generate v=g**x % N
    #   Save everything but x, xH
    v = pow(g, x, N)
    print "  Generate v=g**x % N:", v
    print "  Save everything but x, xH"
    print ""

    # C->S: Send I, A=g**a % N (a la Diffie Hellman)
    print "C->S: Send I, A=g**a % N (a la Diffie Hellman)"
    a = crypto_random(32)
    A = pow(g, a, N)
    print "I:", I
    print "A:", A
    print ""

    # S->C: Send salt, B=kv + g**b % N
    print "S->C: Send salt, B=kv + g**b % N"
    print "salt", salt
    b = crypto_random(32)
    B = k * v + pow(g, b, N)
    print "B:", B
    print ""

    # S, C: Compute string uH = SHA256(A|B), u = integer of uH
    print "S, C: Compute string uH = SHA256(A|B), u = integer of uH"
    u_sha256_generator = hashlib.sha256()
    u_sha256_generator.update(Message().set_int(A).to_str() + Message().set_int(B).to_str())
    u = int(u_sha256_generator.hexdigest(), 16)
    print "u:", u
    print ""

    # C:
    #   Generate string xH=SHA256(salt|password)
    #   Convert xH to integer x somehow (put 0x on hexdigest)
    print "  Generate string xH=SHA256(salt|password)"
    print "  Convert xH to integer x somehow (put 0x on hexdigest)"
    #   Generate S = (B - k * g**x)**(a + u * x) % N
    print "  Generate S = (B - k * g**x)**(a + u * x) % N"
    # buff = B - k * g**x
    S_c = pow(B - k * pow(g, x, N), a + u * x, N)
    print "S:", S_c
    #   Generate K = SHA256(S)
    print "  Generate K = SHA256(S)"
    K_c_sha256_generator = hashlib.sha256()
    K_c_sha256_generator.update(Message().set_int(S_c).to_str())
    K_c = int(K_c_sha256_generator.hexdigest(), 16)
    print "K:", K_c
    print ""

    # S:
    #   Generate S = (A * v**u) ** b % N
    print "  Generate S = (A * v**u) ** b % N"
    S_s = pow(A * pow(v, u, N), b, N)
    print "S:", S_s
    #   Generate K = SHA256(S)
    print "  Generate K = SHA256(S)"
    K_s_sha256_generator = hashlib.sha256()
    K_s_sha256_generator.update(Message().set_int(S_s).to_str())
    K_s = int(K_s_sha256_generator.hexdigest(), 16)
    print "K:", K_s
    print ""

    # C->S: Send HMAC-SHA256(K, salt)
    signature_c = hmac.HMAC(Message().set_int(K_c).to_str(), salt_str, hashlib.sha256).hexdigest()
    print "C->S: Send HMAC-SHA256(K, salt)"
    print "HMAC-SHA256(K, salt):", signature_c
    print ""

    # S->C: Send "OK" if HMAC-SHA256(K, salt) validates
    signature_s = hmac.HMAC(Message().set_int(K_s).to_str(), salt_str, hashlib.sha256).hexdigest()
    print "S->C: Send \"OK\" if HMAC-SHA256(K, salt) validates"
    try:
        assert signature_s == signature_c
    except AssertionError:
        print "ERROR: Signatures are not equal!!"
    else:
        print "OK: Signature validates"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Implement Secure Remote Password (SRP) - Challenge 35 (Set 5) of Matasano Crypto Challenge.'
    )
    args = parser.parse_args()

    main(args)
