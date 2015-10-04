
import socket
import hashlib
import hmac
import json

from Message import Message
from utils import crypto_random
from socket_wrapper import socket_send, socket_receive, get_server_socket

def check_credentials(sock):
    # C & S: Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    N = 0x009f4f57c0d386b90c5cf147d96466c5c7b2d154e7d32a58695191847f58f5e2ca9c28b497ae1b31d1c2507b1c489662a9d39c5b5100503888cfd7c762a7c1310d26b8ae38ad8de4ba3ff800022221c73be2da3113b4a7ba404a32a446adb9dedb2958bab3b26f2984396e1af1fc28594182b2a72de7fed99ea03e34c0d69e02db
    g = 2
    k = 3
    I = 'example@mail.com'
    P = 'somepassword1234'

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
    print "  Convert xH to integer x somehow (put 0x on hexdigest):"
    print "x", x

    #   Generate v=g**x % N
    #   Save everything but x, xH
    v = pow(g, x, N)
    print "  Generate v=g**x % N:", v
    print "  Save everything but x, xH"
    print ""

    values = socket_receive(sock)
    for key, value in values.iteritems():
        globals()[key] = value
    assert I
    assert A
    print 'Received variables I and A'
    print "I:", I
    print "A:", A
    print ""

    # S->C: Send salt, B=kv + g**b % N
    b = crypto_random(32)
    B = k * v + pow(g, b, N)
    data = json.dumps({'salt': salt, 'B': B})
    socket_send(sock, data)
    print "S->C: Send salt, B=kv + g**b % N"
    print ""

    # S, C: Compute string uH = SHA256(A|B), u = integer of uH
    print "S, C: Compute string uH = SHA256(A|B), u = integer of uH"
    u_sha256_generator = hashlib.sha256()
    u_sha256_generator.update(Message().set_int(A).to_str() + Message().set_int(B).to_str())
    u = int(u_sha256_generator.hexdigest(), 16)
    print "u:", u
    print ""

    # S:
    #   Generate S = (A * v**u) ** b % N
    print "  Generate S = (A * v**u) ** b % N"
    S = pow(A * pow(v, u, N), b, N)
    print "S:", S
    #   Generate K = SHA256(S)
    print "  Generate K = SHA256(S)"
    K_sha256_generator = hashlib.sha256()
    K_sha256_generator.update(Message().set_int(S).to_str())
    K = int(K_sha256_generator.hexdigest(), 16)
    print "K:", K
    print ""

    values = socket_receive(sock)
    for key, value in values.iteritems():
        globals()[key] = value
    assert signature

    signature_s = hmac.HMAC(Message().set_int(K).to_str(), salt_str, hashlib.sha256).hexdigest()
    print "S->C: Send \"OK\" if HMAC-SHA256(K, salt) validates"
    if signature == signature_s:
        print "OK: Signatures match"
        response = "OK"
    else:
        print "ERROR: Signatures don't match"
        response = "ERROR"

    data = json.dumps({'response': response})
    socket_send(sock, data)

def main(args):
    # Get communication socket.
    print "Waiting for connection requests"
    sock = get_server_socket(socket.gethostname(), args.port_number)
    print ""
    try:
        check_credentials(sock)
    finally:
        sock.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="This is the server side of: "
        "Break SRP with a zero key - Challenge 35 (Set 5) of Matasano Crypto Challenge."
    )
    parser.add_argument('port_number',
        help='Port number to connect to', type=int)
    args = parser.parse_args()

    main(args)
