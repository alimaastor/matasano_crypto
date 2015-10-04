
import socket
import hashlib
import hmac
import json
import subprocess
import time
import os

from lib.Message import Message
from lib.utils import crypto_random
from lib.socket_wrapper import socket_send, socket_receive, get_client_socket

def log_in(sock):
    # C & S: Agree on N=[NIST Prime], g=2, k=3, I (email), P (password)
    N = 0x009f4f57c0d386b90c5cf147d96466c5c7b2d154e7d32a58695191847f58f5e2ca9c28b497ae1b31d1c2507b1c489662a9d39c5b5100503888cfd7c762a7c1310d26b8ae38ad8de4ba3ff800022221c73be2da3113b4a7ba404a32a446adb9dedb2958bab3b26f2984396e1af1fc28594182b2a72de7fed99ea03e34c0d69e02db
    g = 2
    k = 3
    I = 'example@mail.com'
    P = 'somepassword1234'

    print "Sending N, g & k to the server."
    data = json.dumps({'N': N, 'g': g, 'k': k})
    socket_send(sock, data)
    print ""

    # C->S: Send I, A=g**a % N (a la Diffie Hellman)
    print "C->S: Send I, A=g**a % N (a la Diffie Hellman)"
    a = crypto_random(32)
    A = pow(g, a, N)
    print "I:", I
    print "A:", A
    print ""

    data = json.dumps({'I': I, 'A': A})
    socket_send(sock, data)

    values = socket_receive(sock)
    for key, value in values.iteritems():
        globals()[key] = value
    assert salt
    assert B
    print 'Received variables salt and B'
    print "salt:", salt
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
    x_sha256_generator = hashlib.sha256()
    x_sha256_generator.update(Message().set_int(salt).to_str() + P)
    x = int(x_sha256_generator.hexdigest(), 16)
    #   Generate S = (B - k * g**x)**(a + u * x) % N
    print "  Generate S = (B - k * g**x)**(a + u * x) % N"
    # buff = B - k * g**x
    S = pow(B - k * pow(g, x, N), a + u * x, N)
    print "S:", S
    #   Generate K = SHA256(S)
    print "  Generate K = SHA256(S)"
    K_sha256_generator = hashlib.sha256()
    K_sha256_generator.update(Message().set_int(S).to_str())
    K = int(K_sha256_generator.hexdigest(), 16)
    print "K:", K
    print ""

    # C->S: Send HMAC-SHA256(K, salt)
    signature = hmac.HMAC(Message().set_int(K).to_str(), Message().set_int(salt).to_str(), hashlib.sha256).hexdigest()
    data = json.dumps({'signature': signature})
    socket_send(sock, data)
    print "C->S: Send HMAC-SHA256(K, salt)"
    print ""

    values = socket_receive(sock)
    for key, value in values.iteritems():
        globals()[key] = value
    assert response
    if response == "OK":
        print "OK: Logged in"
    elif response == 'ERROR':
        print "ERROR: Not logged in"

def main(args):
    # Start server.
    print "Starting the server ..."
    server_path = os.path.join('lib', 'srp_server.py')
    server_logfile = os.path.join("/tmp", "srp_server.log")
    with open(server_logfile, 'w+') as devnull:
        server_process = subprocess.Popen(
            'python {} {}'.format(server_path, str(args.port_number)),
            shell=True,
            stdout=devnull,
            stderr=devnull)
    time.sleep(2)
    ret = server_process.poll()
    if ret != None:
        print "Server has not started correctly. Port already in use?"
        exit(1)

    # Get communication socket.
    sock = get_client_socket(args.hostname, args.port_number)
    print "Communications initialised"
    print ""
    try:
        log_in(sock)
    finally:
        sock.shutdown(socket.SHUT_RDWR)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='Implement Secure Remote Password (SRP) - Challenge 35 (Set 5) of Matasano Crypto Challenge.'
    )
    parser.add_argument('hostname',
        help='Address of the host to connect to', type=str)
    parser.add_argument('port_number',
        help='Port number to connect to', type=int)
    args = parser.parse_args()

    main(args)
