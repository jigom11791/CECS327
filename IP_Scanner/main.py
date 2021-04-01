import networkscan
import socket


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
