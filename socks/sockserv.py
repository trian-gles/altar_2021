import socket
import select
import pickle
import os
from random import choice, shuffle
from itertools import cycle
import logging
import datetime


class Server:
    HEADER_LENGTH = 10

    def __init__(self, ip="127.0.0.1", port=8000, deal_time=1, pass_time=1):
        logging.basicConfig(filename="server.log", level=logging.DEBUG, filemode='w')
        self.print_log(f"Building server on IP {ip}, PORT {port}")
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, port))
        self.server_socket.listen()

        self.sockets_list = [self.server_socket]

        # dictionary containing socket objects that point to usernames
        self.clients = {}

        # circular list to be later created
        self.turn_iter = None
        # The mode will go from "sleep" to "play" to "finish" to "quit"

        self.mode = "sleep"

    def print_log(self, msg):
        print(msg)
        logging.debug(str(datetime.datetime.now()) + " : " + msg)

    def send_pickle(self, content_dict, send_sock):
        dict_pick = pickle.dumps(content_dict)
        pick_mess = bytes(f"{len(dict_pick):<{Server.HEADER_LENGTH}}", "utf-8") + dict_pick
        send_sock.send(pick_mess)

    def receive_message(self, client_socket):
        try:
            message_header = client_socket.recv(Server.HEADER_LENGTH)

            if not len(message_header):
                return False

            message_length = int(message_header.decode('utf-8').strip())
            return {"header": message_header,
                    "data": client_socket.recv(message_length)}
        except:
            return False

    def register_client(self):
        # add the client to the list of sockets and dictionary of clients
        client_socket, client_addr = self.server_socket.accept()

        user = self.receive_message(client_socket)
        if user is False:
            return

        self.sockets_list.append(client_socket)
        self.clients[client_socket] = user

        self.print_log(f"accepted new connection from \
        {client_addr[0]}: {client_addr[1]} username = {user['data'].decode('utf-8')}")

    def remove_client(self, notified_socket):
        # disconnect from the indicated socket
        self.print_log(f"Closed connection from {self.clients[notified_socket]['data'].decode('utf-8')}")
        self.sockets_list.remove(notified_socket)
        del self.clients[notified_socket]

    def handle_exception_socks(self, exception_sockets):
        # delete sockets throwing errors
        for notified_socket in exception_sockets:
            self.sockets_list.remove(notified_socket)
            del self.clients[notified_socket]

    def start_piece(self):
        self.mode = "play"
        self.turn_iter = cycle(self.sockets_list[1:])
        deck = tuple(range(15))
        init_content = ((None, None, None), (None, None, None), (None, None, None), deck)
        self.new_turn_update(init_content)

    def new_turn_update(self, gui_content: tuple):
        current_sock = next(self.turn_iter)
        current_name = self.clients[current_sock]['data'].decode('utf-8')
        content_dict = {"method": "update", "content": gui_content,
                        "current_player": current_name}
        print(gui_content)
        for sock in self.sockets_list:
            if sock != self.server_socket:
                self.send_pickle(content_dict, sock)

    def listen(self):
        read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)

        for notified_socket in read_sockets:
            if notified_socket == self.server_socket:
                self.register_client()

            else:
                message = self.receive_message(notified_socket)

                if message is False:
                    self.remove_client(notified_socket)
                    continue

                user = self.clients[notified_socket]
                username = user['data'].decode('utf-8')
                msg_dict = pickle.loads(message['data'])

                self.print_log(f"received message from {user['data'].decode('utf-8')}: {msg_dict}")

                if msg_dict["method"] == "quit":
                    self.mode = "quit"
                elif msg_dict["method"] == "start":
                    if self.mode == "sleep":
                        self.start_piece()
                        self.print_log(f"User {username} has initiated the piece")
                elif msg_dict["method"] == "end_turn":
                    self.new_turn_update(msg_dict["content"])


if __name__ == "__main__":
    server = Server()
    while True:
        server.listen()
        if server.mode == "quit":
            break