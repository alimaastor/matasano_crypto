
import socket
import hashlib
import hmac
import json

from Message import Message
from utils import crypto_random
from socket_wrapper import socket_send, socket_receive, get_server_socket

I = 'example@mail.com'
P = 'somepassword1234'

def check_credentials(sock):
    # C & S: Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    print "Waiting for client to send us N, g & k. I (email) & P (password) are already known."
    values = socket_receive(sock)
    for key, value in values.iteritems():
        globals()[key] = value
    assert N != None
    assert g != None
    assert k != None
    print "N:", N
    print 'g:', g
    print "k:", k
    print ""

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
    assert I != None
    assert A != None
    print 'Received variables I and A'
    print "I:", I
    print "A:", A
    print ""

    # S->C: Send salt, B=kv + g**b % N, u = 128 bit random number
    b = crypto_random(32)
    B = k * v + pow(g, b, N)
    u = crypto_random(16)
    data = json.dumps({'salt': salt, 'B': B, 'u': u})
    socket_send(sock, data)
    print "S->C: Send salt, B = k * v + g ** b % N, u = 128 bit random number"
    print ""

    # S
    print "S:"
    # S = (A * v ** u)**b % n
    print "  Generate S = (A * v**u) ** b % N"
    S = (A * pow(v, u, N), b, N)
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
    assert signature != None

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
        print "Shutting down socket"
        sock.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="This is a simplified version of the SRP server - Set 5 of Matasano Crypto Challenge."
    )
    parser.add_argument('port_number',
        help='Port number to connect to', type=int)
    args = parser.parse_args()

    main(args)
