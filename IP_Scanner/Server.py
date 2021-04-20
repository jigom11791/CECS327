from socket import *


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.bind((self.host, self.port))
        (self.conn, self.addr) = self.s.accept()

    def run(self):
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            self.conn.send(str(data) + "*")
        self.conn.close()

