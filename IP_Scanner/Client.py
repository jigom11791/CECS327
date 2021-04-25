import socket

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s. connect((socket.gethostname(), 7159))

full_message = ''

while True:
    # 1024 is the data buffer
    msg = s.recv(8)
    if len(msg) <= 0:
        break
    else:
        full_message += msg.decode("utf-8")

print(full_message)
