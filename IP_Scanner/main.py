import PortScanner as ps
import Client
from Server import Server
import hashing
import threading
import logging
import os

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
def send_file(node, file):
    Client.send_file(node, FILE_PORT, file)


def send_file_request(file_list):
    for node in NODES:
        print(node)
        for file in file_list:
            send = Client.send_file_request(node, COMM_PORT, file)
            if send:
                send_file(node, file[0])


def hash_files():
    # os.chdir("sync")  # Changed Directory to sync folder
    for files in os.listdir():  # iterates through folder
       hashing.add_to_dict(files)  # hashes files and this function auto adds to dictionary
    # os.chdir("..")


def check_changes():
    array = []
    # 1. check if any files have been added.
    # os.chdir("sync")  # Changed Directory to sync folder
    for files in os.listdir():
        if not hashing.check_same(files):
            time_modified = os.path.getmtime(files)
            array.append([files, hashing.hash_file(files), time_modified])
    store_changes(array)
    # os.chdir("..")
    return array


def store_changes(array):
    for items in array:
        hashing.dictionary_hash[items[0]] = items[1]


def file_listener():
    array = check_changes()
    if array:
        logging.info("[FILE LISTENER] Files changed, starting request")
        send_file_request(array)
    else:
        logging.info("[FILE LISTENER] No changes in files")


def beginning_check():
    # convert dictionary to a list things
    array = []
    # os.chdir("sync")  # Changed Directory to sync folder
    for files, hash in hashing.dictionary_hash.items():
        time_modified = os.path.getmtime(files)
        array.append([files, hash, time_modified])
    send_file_request(array)
    # os.chdir("..")
    print("IN HERE ")
  #  s.enter(60, 1, beginning_check, (s,))


def looper():
    threading.Timer(6.0, looper).start() #10 seconds
    file_listener()


if __name__ == "__main__":
    os.chdir('sync')
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

    while True:
        logging.info('Searching for nodes\n\n')
        nodes = ps.check_ports(COMM_PORT)
        if len(nodes) > 0:
            add_nodes(nodes)
            break
    # Search for other nodes
    hash_files()
    beginning_check()

    #  beginning_check_no_timer()
    looper()  # loops?
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
            send_file(NODES[0], 'test.txt')
        elif x == "3":
            logging.info(f"Nodes: {NODES} ")
        elif x == "4":
            check_changes()
        add_nodes(comm_server.nodes)







