import socket
import logging
import os

FORMAT = 'utf-8'
SIZE = 1024 * 4
SEP = '<SEP>'


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
                self.__greet__(clientsocket)
            if request == '2':
                self.__receive_file__(clientsocket)

            clientsocket.close()

    def __greet__(self, conn):
        conn.send(bytes("Welcome to the server!", "utf-8"))

    def __receive_file__(self, conn):
        conn.send(f'file transfer request received'.encode(FORMAT))
        rec = conn.recv(SIZE).decode()
        logging.info(f"{rec}")
        filename, filesize = rec.split(SEP)
        filename = os.path.basename(filename)
        filesize = int(filesize)
        logging.info(f'[SERVER] File: {filename} {filesize}bytes')
        filename = "sync/" + str(filename)
        logging.info(f'{filename}')
        file = open(filename, "wb")
        while True:
            logging.info("[SERVER] Getting Data")
            data = conn.recv(SIZE)
            if not data:
                logging.info("[SERVER] Data transfer complete")
                break
            file.write(data)
        file.close()
