//
// Created by Jost Luebbe on 2019-09-02.
//
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <ctype.h>

#define PORT 12000

int main() {
    int socket_fd, client_sock, c, read_size;
    struct sockaddr_in server, client;
    char client_message[2000];

    if ((socket_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1) {
        perror("could not create socket");
        exit(EXIT_FAILURE);
    }
    puts("socket successfully created");

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = inet_addr("127.0.0.1");
    server.sin_port = htons(PORT);

    if (bind(socket_fd, (struct sockaddr *) &server, sizeof(server)) < 0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    if(listen(socket_fd, 3) < 0){
        perror("listen failed");
        exit(EXIT_FAILURE);
    };

    puts("Waiting for incoming connections...");
    c = sizeof(struct sockaddr_in);

    do{
        if ((client_sock = accept(socket_fd, (struct sockaddr *) &client, (socklen_t *) &c)) < 0) {
            perror("accept failed");
            exit(EXIT_FAILURE);
        }

        read_size = recv(client_sock, client_message, 2000, 0);

        char new_str[read_size];

        int i;
        for (i = 0; i < read_size; i++){
            new_str[i] = toupper(client_message[i]);
        }
        new_str[i] = '\0';

        write(client_sock, new_str, strlen(new_str));
        close(client_sock);
    }
    while (1);

    return 0;
}
