import socket
import logging
import os
import hashing
import PortScanner as ps

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
            client_socket, address = self.s.accept()
            logging.info(f"[SERVER] Connection from {address} has been established!")
            if address not in self.nodes and address != ps.IP:
                self.nodes.append(address[0])
            request = client_socket.recv(1024).decode(FORMAT)
            logging.info(f'[SERVER] Request recieved: {request}')
            if request == '0':
                self.__greet__(client_socket)
            elif request == '1':
                self.__receive_file_request__(client_socket)
            elif request == '2':
                self.__receive_file__(client_socket)

            client_socket.close()

    def __greet__(self, conn):
        conn.send(bytes("Welcome to the server!", "utf-8"))

    def __receive_file__(self, conn):
        conn.send(f'file transfer request received'.encode(FORMAT))
        rec = conn.recv(SIZE).decode()
        logging.info(f"{rec}")
        filename, file_size = rec.split(SEP)
        filename = os.path.basename(filename)
        file_size = int(file_size)
        logging.info(f'[SERVER] File: {filename} {file_size}bytes')
        filename = str(filename)
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

    def __receive_file_request__(self, conn):
        # Get filename
        conn.send("starting file transfer request".encode(FORMAT))
        received_message = conn.recv(SIZE).decode(FORMAT)
        file_name, file_hash, edit_time = received_message.split(SEP)
        # logging.info(f'[SERVER] File name received: {file_name}')
        # logging.info(f'[SERVER] File hash received: {file_hash}')
        # logging.info(f'[SERVER] Edit time received: {edit_time}')
        # logging.info('[Server] Checking file')

        logging.info(f'file in dict {file_name in hashing.dictionary_hash}')
        if file_name in hashing.dictionary_hash:
            logging.info(f'hash the same: {hashing.dictionary_hash[file_name] == file_hash}')
            if hashing.dictionary_hash[file_name] == file_hash:
                logging.info(os.path.abspath(os.path.curdir))
                time = os.path.getmtime(str(file_name))
                logging.info(f'{edit_time} > {time}: {float(edit_time) > time}')
                if float(edit_time) > time:
                    send_file = True
                else:
                    send_file = False
            else:
                send_file = True
        else:
            send_file = True

        if not send_file:
            logging.info(f'[SERVER] {file_name} is already up to date')
            conn.send('0'.encode(FORMAT))
        else:
            logging.info(f'[SERVER] {file_name} needs to be updated')
            conn.send('1'.encode(FORMAT))
