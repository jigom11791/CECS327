from time import sleep
import socket
import ipaddress
import threading

max_threads = 50
final = []


def get_my_ip():
    my_ip_address = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
    return my_ip_address


def get_ip_str():
    ip = get_my_ip()
    counter = 0
    for i in range(len(ip)):
        if ip[i] == '.':
            counter += 1
            if counter == 3:
                print(ip[:(i-len(ip))]+".0/24")
                return ip[:(i-len(ip))]+".0/24"
                break


def check_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        socket.setdefaulttimeout(2.0) # seconds (float)
        result = sock.connect_ex((ip, port))
        if result == 0:
            # print ("Port is open")
            final.append(ip)
        # else:
            # print ("Port is closed/filtered")
            # final[ip] = "CLOSED"
        sock.close()
    except:
        pass


def check_ports():
    port = 7159
    ip_str = get_ip_str()
    for ip in ipaddress.IPv4Network(ip_str):
        threading.Thread(target=check_port, args=[str(ip), port]).start()
        if len(final) != 0:
            break
        # sleep(0.1)

    # limit the number of threads.
    while threading.active_count() > max_threads:
        sleep(1)

    print(final)
    return final

