from time import sleep
import socket
import ipaddress
import threading

# Message encoding format
FORMAT = 'utf-8'
max_threads = 50
nodes = []
# This is the node's IP address
IP = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]


# Gets the node's ip address
def get_my_ip():
    my_ip_address = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
    return my_ip_address


# get the node's subnet using the node's ip address
def get_ip_str():
    ip = IP
    counter = 0
    for i in range(len(ip)):
        if ip[i] == '.':
            counter += 1
            if counter == 3:
                print(ip[:(i-len(ip))]+".0/24")
                return ip[:(i-len(ip))]+".0/24"
                break


###############################################
# check if a port at an ip is open. This is used to discover other nodes
# ip : str - ip address being checked
# port : int - port that is being checked.
####################################################
def check_port(ip, port):
    try:
        # Initialize the port
        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set timeout time
        socket.setdefaulttimeout(2.0)  # seconds (float)
        # Attempt to connect node.
        result = s.connect_ex((ip, port))
        # If it was able to connect and the IP is not the node's own ip
        # then add the node to the node list.
        if result == 0 and ip != IP:
            s.send('0'.encode(FORMAT))
            nodes.append(ip)
        # End connection
        s.close()
    except:
        pass


#####################################################
# Checks if the port is open for all the ip's in this node's subnet
# port : int - port that is being checked if open.
####################################################
def check_ports(port):
    # Get the subnet string
    ip_str = get_ip_str()
    # For every ip in the subnet create a thread to check multiple ip's
    for ip in ipaddress.IPv4Network(ip_str):
        threading.Thread(target=check_port, args=[str(ip), port]).start()

    # limit the number of threads.
    while threading.active_count() > max_threads:
        sleep(1)

    # print the found nodes
    print(nodes)
    return nodes

