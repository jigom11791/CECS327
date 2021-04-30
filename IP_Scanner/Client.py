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


def send_file_request(ip, port, file):
    try:
        # Create socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establish connection
        result = client.connect_ex((ip, port))
        if result == 0:
            client.send('1'.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            logging.info(f'[CLIENT] Message received: {msg}')
            # send file name
            msg = f'{file[0]}{SEP}{file[1]}{SEP}{file[2]}'
            client.send(msg.encode(FORMAT))
            send = client.recv(SIZE).decode()
            client.close()
            logging.info(f'[CLIENT] Message Received: {send}\n\n')
            if bool(int(send)):
                return True
            else:
                return False
        client.close()
        return False
    except:
        return False


