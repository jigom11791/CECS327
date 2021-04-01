import networkscan
import socket

myIpAddress = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
print(myIpAddress)

ips = ['192.168.0.11', '192.168.0.12', '192.168.0.1', '192.168.0.40', '192.168.0.50', '192.168.0.24', '192.168.0.32', '192.168.0.63', '192.168.0.25', '192.168.0.10', '192.168.0.67', '192.168.0.42', '192.168.0.16', '192.168.0.74', '192.168.0.18', '192.168.0.36', '192.168.0.87', '192.168.0.88', '192.168.0.26']
ports = '80'


def isOpen(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


if __name__ == '__main__':

    # Define the network to scan
    my_network = "10.0.0.0/24"

    # Create the object
    my_scan = networkscan.Networkscan(my_network)
    # Run the scan of hosts using pings
    my_scan.run()
    counter = 0
    # Display the IP address of all the hosts found
    for i in my_scan.list_of_hosts_found:
        counter = counter + 1
        if (isOpen(i, 80)):
            print("port %d is open", i)

    print(counter)

