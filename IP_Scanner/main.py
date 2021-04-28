import PortScanner as ps
from Client import Client
from Server import Server
import threading
import logging

COMM_PORT = 7159
FILE_PORT = 7158
NODES = []


def salute_nodes():
    if len(NODES) > 0:
        for node in NODES:
            clientThread = threading.Thread(target=client.greet, args=(node, COMM_PORT))
            clientThread.start()


def add_nodes(nodes):
    for node in nodes:
        if node not in NODES:
            NODES.append(node)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    comm_server = Server(COMM_PORT)
    data_server = Server(FILE_PORT)
    client = Client()

    comm_thread = threading.Thread(target=comm_server.runserver)
    comm_thread.start()
    logging.info("[SERVER] starting server at port %d", COMM_PORT)
    file_thread = threading.Thread(target=data_server.runserver)
    file_thread.start()
    logging.info("[SERVER] starting server at port %d", FILE_PORT)

    add_nodes(ps.check_ports())
    while True:
        x = input('Enter Choice: ')
        if x == '0':
            # salute
            logging.info('salute nodes')
            salute_nodes()
        elif x == '1':
            # request nodes
            logging.info('request nodes')
        elif x == "2":
            # send file
            logging.info("files")
        elif x == "3":
            logging.info(f"Nodes: {NODES} ")
            
        add_nodes(comm_server.nodes)
        


