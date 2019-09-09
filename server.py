#! /usr/bin/env python
from socket import *


def main():
    server_port = 12000
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(1)
    print('The server is ready to receive')
    while 1:
        sock, addr = server_socket.accept()
        print(addr)
        print(sock, addr)
        sock.send(sock.recv(1024).upper())
        sock.close()


if __name__ == "__main__":
    main()
