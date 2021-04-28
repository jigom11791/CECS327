import socket
import logging

FORMAT = 'utf-8'


def greet(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((ip, port))
        if result == 0:
            logging.info(f"[CLIENT] Connecting to server at {ip}")
            s.send('0'.encode(FORMAT))
            msg = s.recv(1024).decode(FORMAT)
            logging.info(f'[CLIENT] Message received: {msg}')
        s.close()
    except ConnectionError:
        pass


def request_nodes(ip, port):
    nodes = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    # idk what im doing. I'm thinking that i can send a number as a code for what to do
    # code 1 will be for requesting the thing
    msg = s.recv(1024).decode(FORMAT)
    logging.info(f'[CLIENT] Message received: {msg}')
    logging.info(f"[CLIENT] Requesting node list from {ip}")
    s.send("1".encode(FORMAT))
    logging.info(f"[CLIENT] Request Sent")

    return nodes

