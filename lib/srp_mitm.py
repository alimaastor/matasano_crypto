
import hashlib
import hmac
import json

from Message import Message
from utils import crypto_random
from socket_wrapper import socket_send, socket_receive, get_server_socket

def main(args):
    pass

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description="This is a MITM for the simplified SRP server - Set 5 of Matasano Crypto Challenge."
    )
    parser.add_argument('port_number',
        help='Port number to connect to', type=int)
    parser.add_argument('server_port_number',
        help='Port number to connect to as a server', type=int)
    args = parser.parse_args()

    main(args)
