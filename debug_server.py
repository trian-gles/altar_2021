from socks import Server

server = Server(ip="127.0.0.1")
while True:
    server.listen()
    if server.mode == "quit":
        server.reset()