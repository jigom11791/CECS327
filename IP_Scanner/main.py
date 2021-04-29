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
def send_file():
    for node in NODES:
        Client.send_file(node, FILE_PORT, 'test.txt')


def send_file_request(file_list):
    for node in NODES:
        Client.send_file_request(node, COMM_PORT, file_list)


def hash_files():
    os.chdir("sync") #Changed Directory to sync folder
    for files in os.listdir(): #iterates through folder
       hashing.add_to_dict(files) #hashes files and this function auto adds to dictionary
    os.chdir("..")
    # find all the files in the sync folder and hash all
    # the files and add them to the dictionary


def check_changes():
    array = []
    # 1. check if any files have been added.\
    os.chdir("sync")  # Changed Directory to sync folder
    for files in os.listdir():
        if not hashing.check_same(files):
            time_modified = os.path.getmtime(files)
        #    print("time modified test ",  time_modified)
         #   print("file name ", files)
            array.append([files, hashing.hash_file1(files), time_modified])
    store_changes(array)
    os.chdir("..")
  #  print("ARRAY IS ", array)
    return array
  #  print("ARRAY IS ", array)
    # 2. hash the files and check if any of them have changed
    # 3. return an array of arrays with that looks like:
    #       [[filename, hash, time_modified], [filename...]]


def store_changes(array):
    for items in array:
        hashing.dictionary_hash[items[0]] = items[1]


def file_listener():
    logging.info("hello in listener")
    array = check_changes()
    if array:
        logging.info("files changed, starting request")
        send_file_request(array)


def beginning_check():
    #cnvert dictionary to a list things
    array = []
    os.chdir("sync")  # Changed Directory to sync folder
    for files, hash in hashing.dictionary_hash.items():
        time_modified = os.path.getmtime(files)
        array.append([files, hash, time_modified])
    send_file_request(array)
    os.chdir("..")
 #   print("begining checks", array)



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
    hash_files()
    beginning_check()
    threading.Timer(60.0, file_listener).start() #request 1 minute!!!

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
        elif x == "4":
            check_changes()
        add_nodes(comm_server.nodes)

# Comment to do

# maybe put file name into dictionary or something
# 1. Hashing function to find what files in the sync(master) folder
#
# 2. Check if the file changed by redoing the hash / check if same
    # or check if the modified file name is same







