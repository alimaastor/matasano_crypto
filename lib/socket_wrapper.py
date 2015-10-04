
import socket
import json

def socket_send(socket, vars):
    def __sendvar(var):
        def __send(data):
            totalsent = 0
            datalen = len(data)
            while totalsent < datalen:
                sent = socket.send(data[totalsent:])
                if sent == 0:
                    raise RuntimeError("socket connection broken")
                totalsent = totalsent + sent
        __send(str(len(var)))
        __send(var)
    __sendvar(vars)

def socket_receive(socket):
    def __receive():
        msglen = []
        while True:
            char = socket.recv(1)
            if not char:
                raise RuntimeError("socket connection broken")
            if char == '{':
                break
            msglen.append(char)
        msglen = int(''.join(msglen))
        msg_in = '{' + socket.recv(int(msglen - 1))
        if not msg_in:
            raise RuntimeError("socket connection broken")
        return msg_in
    msg = __receive()
    return json.loads(msg)

def get_server_socket(hostname, port):
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind((hostname, port))
    serversocket.listen(1)
    (clientsocket, address) = serversocket.accept()
    return clientsocket

def get_client_socket(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((hostname, port))
    return s
