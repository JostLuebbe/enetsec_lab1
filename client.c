//
// Created by Jost Luebbe on 2019-09-02.
//

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <stdlib.h>


#define PORT 5555


int main() {
    int sock;
    struct sockaddr_in server;
    char server_reply[2000];

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket could not be created");
        exit(EXIT_FAILURE);
    }

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_port = htons(PORT);

    if (connect(sock, (struct sockaddr *) &server, sizeof(server)) < 0) {
        perror("client connection");
        exit(EXIT_FAILURE);
    }

    char message[2000];
    printf("Input lowercase sentence: ");
    fgets(message, 2000, stdin);

    if (send(sock, message, strlen(message), 0) < 0) {
        puts("message send failed");
        exit(EXIT_FAILURE);
    }

    bzero(server_reply, 2000);
    if (recv(sock, server_reply, 2000, 0) < 0) {
        puts("server reply failed");
        exit(EXIT_FAILURE);
    }

    printf("Server reply: %s\n", server_reply);

    close(sock);
    return 0;
}
