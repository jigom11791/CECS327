import socket
import logging


class Server:
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), port))
        self.nodes = []

    def runserver(self):
        self.s.listen(5)

        while True:
            clientsocket, address = self.s.accept()
            if address not in self.nodes:
                self.nodes.append(address)
            logging.info(f"[SERVER] Connection from {address} has been established!")
            clientsocket.send(bytes("Welcome to the server!", "utf-8"))
            clientsocket.close()
