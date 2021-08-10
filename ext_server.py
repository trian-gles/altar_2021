from socks import Server

server = Server(ip="")
while True:
    server.listen()
    if server.mode == "quit":
        server.reset()