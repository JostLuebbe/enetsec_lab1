client: client.o client.c
	gcc -o client client.c -I.

server: server.o server.c
	gcc -o server server.c -I.
