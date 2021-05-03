import PortScanner as ps
import Client
from Server import Server
import hashing
import threading
import logging
import os

#establish ports and NODE dictionary
COMM_PORT = 7159
FILE_PORT = 7158
NODES = []

# function salute_nodes mainly used for testing if
# nodes talk to each other.
# will greet each other if connection is established.
def salute_nodes():
    if len(NODES) > 0:
        for node in NODES:
            Client.greet(node, COMM_PORT)


# Add the nodes to the node list if node is not already in list
def add_nodes(nodes):
    for node in nodes:
        if node not in NODES:
            NODES.append(node)


# Send a file to the other nodes
def send_file(node, file):
    Client.send_file(node, FILE_PORT, file)


# Sends a file request to Client
def send_file_request(file_list):
    for node in NODES:
        print(node)
        for file in file_list:
            send = Client.send_file_request(node, COMM_PORT, file)
            if send:
                send_file(node, file[0])


# Hash files function that sends to the hashing class for the hashing and then adds nodes to the dicitonary.
def hash_files():
    # os.chdir("sync")  # Changed Directory to sync folder
    for files in os.listdir():  # iterates through folder
       hashing.add_to_dict(files)  # hashes files and this function auto adds to dictionary
    # os.chdir("..")


# Function check_changes checks for any changes in the master folder.
# Returns an array with the changes, in the following format: [ file name, the hash, and time modified ]
def check_changes():
    array = []
    # os.chdir("sync")  # Changed Directory to sync folder
    for files in os.listdir(): #iterates through folder
        if not hashing.check_same(files): #check if hashing are same and if not
            time_modified = os.path.getmtime(files) #get time modifed
            array.append([files, hashing.hash_file(files), time_modified]) #adds hashing of file and the time modified to an array
    store_changes(array) #stores the array
    # os.chdir("..")
    return array #returns the array for further processing


# Function store_changes takes in an array and then stores the new hash if
# changes to the file are made into the dictionary
def store_changes(array):
    for items in array: #iterates through item being passed
        hashing.dictionary_hash[items[0]] = items[1] #adds to dictionary


# Function file_listener checks if files have changed and if changed, sends a request to other nodes
# if not, it produces a msg that no changes were made.
def file_listener():
    array = check_changes() #calls check_changes function
    if array: #checks if files have changed
        logging.info("[FILE LISTENER] Files changed, starting request")
        send_file_request(array) #sends a request to fix change
    else: #else do nothing because file did not change.
        logging.info("[FILE LISTENER] No changes in files")


def beginning_check():
    # convert dictionary to a list things
    array = []
    # os.chdir("sync")  # Changed Directory to sync folder
    for files, hash in hashing.dictionary_hash.items(): #iterates through dictionary
        time_modified = os.path.getmtime(files) #get time modfiied
        array.append([files, hash, time_modified]) #appends to array
    send_file_request(array) #sends request to change files
    # os.chdir("..")
  #  s.enter(60, 1, beginning_check, (s,))

# Function Looper loops through file_listener function every 6 seconds to check if the files are the same throughout
def looper():
    threading.Timer(30.0, looper).start() #utilizing threading timer function to start looping this method every 30 seconds
    file_listener() # when function loops, this function is called


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
    hash_files() #calls initial hash to hash all files
    beginning_check() #runs beginning checks on program to see if any changes are made.
    looper()  # runs function in the background every 30 seconds to check for changed files.
    # Main loop
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
            # send files
            send_file(NODES[0], 'test.txt')
        elif x == "3":
            logging.info(f"Nodes: {NODES} ")
        elif x == "4":
            #check for changes
            check_changes()
        add_nodes(comm_server.nodes)







