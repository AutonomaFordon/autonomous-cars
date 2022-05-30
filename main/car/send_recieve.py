import socket
import json
import sys
sys.path.append("../resources/")
from protocols import *

conf_key="Ghent2021!"

# connect to the server
def socket_connect():
    global host
    global port
    global sock
    host = "192.168.0.5"
    port = 5005
    sock = socket.socket()
    try:
        # Connect
        sock.connect((host, port))
        # Recieve a establish_conn protocol, this part is a handshake
        # between the server and the device
        answer = sock.recvfrom(1024)
        answer = answer.decode("utf-8")
        #print(str(answer))
        answer = json.loads(answer)
        sock.send(conf_key)
    except socket.error as msg:
        print("Error trying to connect to socket: "+str(msg))
        print("Retrying...")
        socket_connect()

socket_connect()
