from socks import Server
import socket

server = Server(ip=socket.gethostbyname(socket.gethostname()))

while True:
    server.listen()
    if server.mode == "quit":
        break