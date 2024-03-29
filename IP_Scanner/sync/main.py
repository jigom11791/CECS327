import PortScanner as ps
import Client
from Server import Server
import hashing
import threading
import logging

COMM_PORT = 7159
FILE_PORT = 7158
NODES = []


           # file = open("test.txt", "rb")
           # hashing.add_to_dict(file)
           # file2 = open("test.txt", "rb")
           # print(hashing.checkSame(file2))
           # print(hashing.dictionary_hash)

def salute_nodes():
    if len(NODES) > 0:
        for node in NODES:
            Client.greet(node, COMM_PORT)


def add_nodes(nodes):
    for node in nodes:
        if node not in NODES:
            NODES.append(node)


def send_file():
    for node in NODES:
        Client.send_file(node, FILE_PORT, 'main.py')


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    comm_server = Server(COMM_PORT)
    data_server = Server(FILE_PORT)

    comm_thread = threading.Thread(target=comm_server.runserver)
    comm_thread.start()
    logging.info("[SERVER] starting server at port %d", COMM_PORT)
    file_thread = threading.Thread(target=data_server.runserver)
    file_thread.start()
    logging.info("[SERVER] starting server at port %d", FILE_PORT)

    add_nodes(ps.check_ports(COMM_PORT))

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
            send_file()
        elif x == "3":
            logging.info(f"Nodes: {NODES} ")

        add_nodes(comm_server.nodes)



# Comment to do



#maybe put file name into dictionary or something
# 1. Hashing function to find what files in the sync(master) folder
#
# 2. Check if the file changed by redoing the hash / check if same
        #or check if the modified file name is same







