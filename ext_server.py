from socks import Server
while True:
    server = Server()

    while True:
        server.listen()
        if server.mode == "quit":
            break