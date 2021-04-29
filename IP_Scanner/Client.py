import socket
import logging
import os

FORMAT = 'utf-8'
SIZE = 1024*4
SEP = '<SEP>'


def greet(ip, port):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client.connect_ex((ip, port))
        if result == 0:
            logging.info(f"[CLIENT] Connecting to server at {ip}")
            client.send('0'.encode(FORMAT))
            msg = client.recv(1024).decode(FORMAT)
            logging.info(f'[CLIENT] Message received: {msg}')
        client.close()
    except (ConnectionError, ConnectionResetError, ConnectionRefusedError):
        pass


def send_file(ip, port, filename):
    try:
        file_size = os.path.getsize(filename)
        logging.info(f'[CLIENT] connecting to file server.')
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client.connect_ex((ip, port))
        if result == 0:
            # Send message that it wants to send file
            client.send('2'.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            logging.info(f'[CLIENT] Message Received: {msg}')
            # Send file name and file size
            client.send(f"{filename}{SEP}{file_size}".encode())

            file = open(filename, 'rb')

            while True:
                data = file.read(SIZE)

                if not data:
                    break
                client.sendall(data)
        client.close()
    except:
        pass


def send_file_request(ip, port, file_list):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client.connect_ex((ip, port))
        if result == 0:
            for file in file_list:
                client.send(file[0].encode(FORMAT))
                msg = client.recv(SIZE).decode(FORMAT)
                logging.info(f'[CLIENT]: Message received: {msg}')
                client.send(file[1].enconde(FORMAT))

        else:
            pass
        client.close()
    except:
        pass


