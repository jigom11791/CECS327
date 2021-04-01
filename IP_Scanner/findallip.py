import networkscan
import socket

if __name__ == '__main__':

    # define the network to scan
    my_network="192.168.0.0/24"

    # create the object
    my_scan = networkscan.Networkscan(my_network)

    # run the scan of hosts using pings
    my_scan.run()
    print(my_scan.list_of_hosts_found)
