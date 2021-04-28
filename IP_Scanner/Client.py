import socket
import logging

ENC = 'utf-8'

class Client:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def greet(self, ip, port):
        logging.info(f"[CLIENT] Connecting to server at {ip} using port {port}")
        self.s.connect((ip, port))

        msg = self.s.recv(1024).decode(ENC)
        logging.info(f'[Client] Message received: {msg}')
        self.s.close()

    def request_nodes(self, ip, port):
        nodes = []
        self.s.connect((ip, port))
        # idk what im doing. I'm thinking that i can send a number as a code for what to do
        # code 1 will be for requesting the thing
        msg = self.s.recv(1024).decode(ENC)
        logging.info(f'[CLIENT] Message received: {msg}')
        logging.info(f"[CLIENT] Requesting node list from {ip}")
        self.s.send("1".encode(ENC))
        logging.info("[CLIENT] Request Sent")

        return nodes

