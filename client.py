#! /usr/bin/env python
from socket import *


def main():
    server_ip = '127.0.0.1'
    server_port = 8080
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    user_input = input("Input lowercase sentence: ")
    client_socket.send(user_input.encode())
    print(f'From Server: {client_socket.recv(1024).decode()}')
    client_socket.close()


if __name__ == "__main__":
    main()
