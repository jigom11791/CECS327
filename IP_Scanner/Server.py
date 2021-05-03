import socket
import logging
import os
import hashing
import PortScanner as ps

FORMAT = 'utf-8'  # Encoding format for sending messages
SIZE = 1024 * 4  # Buffer size
SEP = '<SEP>'  # Separator for multi - value messages


#####################################################
# Server class. Unlike the client, the server does not stop, it runs for
# the whole time the program is running
#########################################################
class Server:
    # Server constructor.
    # port : int - this is the port that the server uses to communicate
    def __init__(self, port):
        # initialize the server socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the server socket to the servers ip and specified port number
        self.s.bind((socket.gethostname(), port))
        # keep track of the nodes that connect to it.
        self.nodes = []

    # Run the server.
    def runserver(self):
        # Listen for incoming connections.
        # It can have at most 5 incoming connections at a time?
        self.s.listen(5)

        # Run the server until the program is closed
        while True:
            # If a node attempts to connect to it, accept the connection
            client_socket, address = self.s.accept()

            # If the connecting address is not the nodes own address display message
            if address != ps.IP:
                logging.info(f"[SERVER] Connection from {address} has been established!\n\n")
            # if address is not in node list and is not it's own address, add to node list
            if address not in self.nodes and address != ps.IP:
                self.nodes.append(address[0])

            # Receive request code
            request = client_socket.recv(1024).decode(FORMAT)
            # Print request code
            logging.info(f'[SERVER] Request recieved: {request}')
            # Request code '0' is mainly for testing purposes. It just greets all the nodes in the node list.
            if request == '0':
                self.__greet__(client_socket)
            # Request code '1' is used to send a request to send file.
            elif request == '1':
                self.__receive_file_request__(client_socket)
            # Request code '2' is used to send a file.
            elif request == '2':
                self.__receive_file__(client_socket)

            # Close connection with the client once it processes the request.
            client_socket.close()

    # Send message welcome message
    def __greet__(self, conn):
        conn.send(bytes("Welcome to the server!", "utf-8"))

    # Receive file from the server
    def __receive_file__(self, conn):
        # Send message to confirm that request was received.
        conn.send(f'server ready to receive file'.encode(FORMAT))

        # Receive file name
        file_name = conn.recv(SIZE).decode()
        # open file name. If file does not exist, it creates the file.
        file = open(file_name, "wb")

        # While the client is still sending the files, the server will receive the data
        while True:
            logging.info("[SERVER] Getting Data")
            data = conn.recv(SIZE)
            if not data:
                logging.info("[SERVER] File transfer complete/n/n")
                break
            # Write the data to the file
            file.write(data)
        # Close the file
        file.close()

    # Check if the file can be sent to the server.
    def __receive_file_request__(self, conn):
        # Send confirmation that the request was received.
        conn.send("starting file transfer request".encode(FORMAT))
        # Receive file information
        received_message = conn.recv(SIZE).decode(FORMAT)
        # The message has multiple values separated by separator string.
        # Separate the values.
        file_name, file_hash, edit_time = received_message.split(SEP)

        # Check if the file can be sent.
        # First check if the file is in the hash dictionary.
        # logging.info(f'file in dict {file_name in hashing.dictionary_hash}')
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
