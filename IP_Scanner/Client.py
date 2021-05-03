import socket
import logging
import os

# This is the encoding for the messages that are being sent
FORMAT = 'utf-8'
# This is the buffer size for the messages
SIZE = 1024*4
# This is a separator used to send many values with a single message
SEP = '<SEP>'

################################################################
# This is mainly test code to test sending a message to the other nodes
# ip : str - the server ip
# port : int - the port used to communicate. The port should be COMM_PORT
#################################################################
def greet(ip, port):
    try:
        # Initialize the client
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Start a connection, and recieve an error code. If there is no
        # error then it returns 0
        result = client.connect_ex((ip, port))
        # If there was no connection error
        if result == 0:
            logging.info(f"[CLIENT] Connecting to server at {ip}")
            # Send request code. Request code '0' lets the server know that the
            # client just want to say hi
            client.send('0'.encode(FORMAT))
            # Receive a message from the server.
            msg = client.recv(1024).decode(FORMAT)
            # Print out the message
            logging.info(f'[CLIENT] Message received: {msg}\n\n')
        # Close the connection. A connection has to be established every time the
        # the node want to communicate with the server
        client.close()
    except (ConnectionError, ConnectionResetError, ConnectionRefusedError):
        logging.info(f"[CLIENT] Greeting failed.\n\n")
        pass


############################################################################
# This function allows to send the file with the specified file name,
# to the node at the specified ip, using the specified port. The port should
# be the FILE_PORT.
# ip : str - the server ip
# port : int - the port used to send the file. This should be the FILE_PORT
# file_name : str - the file name
############################################################################
def send_file(ip, port, file_name):
    try:
        logging.info(f'[CLIENT] connecting to file server.')
        # instantiate socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = client.connect_ex((ip, port))
        if result == 0:
            # Send message code '2':
            # Message code 2 tells the server that the client is sending a file.
            client.send('2'.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            logging.info(f'[CLIENT] Message Received: {msg}')
            # Send file name and file size
            client.send(f"{file_name}".encode())
            # Open the file that is going to be sent
            file = open(file_name, 'rb')

            # Read the file and send it in pieces until the whole file is sent
            while True:
                data = file.read(SIZE)

                if not data:
                    break
                client.sendall(data)

        # End connection
        client.close()
        logging.info('[CLIENT] File Transfer complete.\n\n')
    except:
        # If the file transfer filed print fail message
        logging.info('[CLIENT] File transfer failed\n\n.')


####################################################################
# Send request send the file to the server
# ip : string - the server ip
# port : int - the port used to communicate. It should be the COMM_PORT
# file - this is an array with file information. it contains :
#       [file_name: string, file_hash : string, edit_time : double]
# if the server return true then the the function will return true, otherwise it will return false
#####################################################################
def send_file_request(ip, port, file):
    try:
        # Create socket
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Establish connection
        result = client.connect_ex((ip, port))
        if result == 0:
            # Send the server request code '1':
            # request code 1 lets the server know that the client wants to send
            client.send('1'.encode(FORMAT))

            # Receive message from the server.
            # This is partially cosmetic and partially to seperate the two messages that the client is sending
            msg = client.recv(SIZE).decode(FORMAT)
            # Print the message
            logging.info(f'[CLIENT] Message received: {msg}')
            # send file name, file hash, and modified time
            msg = f'{file[0]}{SEP}{file[1]}{SEP}{file[2]}'
            client.send(msg.encode(FORMAT))

            # Get response from the server.
            # If the Client can send the file, then send is '1' else it is '0'
            send = client.recv(SIZE).decode()

            # End the client connection
            client.close()
            logging.info(f'[CLIENT] Message Received: {send}\n\n')

            # If send is true then return true, otherwise return false.
            if bool(int(send)):
                return True
            else:
                return False

        # End connection with the server
        client.close()
        return False
    except:
        return False


