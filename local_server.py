from socks import Server

server = Server()

while True:
    server.listen()
    if server.mode == "quit":
        break