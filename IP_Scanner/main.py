import PortScanner as ps
import Client
from Server import Server
import hashing
import threading
import logging

COMM_PORT = 7159
FILE_PORT = 7158
NODES = []


# Mainly for testing purposes
def salute_nodes():
    if len(NODES) > 0:
        for node in NODES:
            Client.greet(node, COMM_PORT)


# Add the nodes to the node list
def add_nodes(nodes):
    for node in nodes:
        if node not in NODES:
            NODES.append(node)


# Send a file to the other nodes
def send_file():
    for node in NODES:
        Client.send_file(node, FILE_PORT, 'test.txt')


def send_file_request(file_list):
    for node in NODES:
        Client.send_file_request(node, COMM_PORT, file_list)


def hash_files():
    # find all the files in the sync folder and hash all
    # the files and add them to the dictionary
    pass


def check_changes():
    # 1. check if any files have been added.
    # 2. hash the files and check if any of them have changed
    # 3. return an array of arrays with that looks like:
    #       [[filename, hash, time_modified], [filename...]]
    pass


if __name__ == "__main__":
    # Format for the logging messages
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")

    # Instantiate the servers
    comm_server = Server(COMM_PORT)
    data_server = Server(FILE_PORT)
    # Start the server threads
    comm_thread = threading.Thread(target=comm_server.runserver)
    comm_thread.start()
    logging.info("[SERVER] starting server at port %d", COMM_PORT)
    file_thread = threading.Thread(target=data_server.runserver)
    file_thread.start()
    logging.info("[SERVER] starting server at port %d", FILE_PORT)

    # Search for other nodes
    add_nodes(ps.check_ports(COMM_PORT))

    # Main loop for testing purposes.
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

# maybe put file name into dictionary or something
# 1. Hashing function to find what files in the sync(master) folder
#
# 2. Check if the file changed by redoing the hash / check if same
    # or check if the modified file name is same







