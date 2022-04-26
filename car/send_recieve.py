import socket
import json
import sys
sys.path.append("../resources/")
from protocols import *

conf_key="Ghent2021!"

def socket_connect():
    global host
    global port
    global sock
    host = "192.168.0.3"
    port = 5005
    sock = socket.socket()
    try:
        sock.connect((host, port))
        answer = sock.recvfrom(1024)
        answer = bytes(answer, "utf-8")
        hs_req(answer)
        if (answer.get_typeof()=="establish_conn"):
            print("hej")
        #answer = json.loads(answer)
        sock.send(bytes(conf_key))
    except socket.error as msg:
        print("Error trying to connect to socket: "+str(msg))
        print("Retrying...")
        socket_connect()

socket_connect()
