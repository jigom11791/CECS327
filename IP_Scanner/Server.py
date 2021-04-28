import socket
import logging

FORMAT = 'utf-8'


def greet(clientsocket):
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))


class Server:
    def __init__(self, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((socket.gethostname(), port))
        self.nodes = []

    def runserver(self):
        self.s.listen(5)

        while True:
            clientsocket, address = self.s.accept()
            logging.info(f"[SERVER] Connection from {address} has been established!")
            if address not in self.nodes:
                self.nodes.append(address[0])
            request = clientsocket.recv(1024).decode(FORMAT)
            logging.info(f'[SERVER] Request recieved: {request}')
            if request == '0':
                greet(clientsocket)

            clientsocket.close()
