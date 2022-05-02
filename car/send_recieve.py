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
    host = "192.168.0.5"
    port = 5005
    sock = socket.socket()
    try:
        sock.connect((host, port))
        answer = sock.recvfrom(1024)
        #answer = answer.decode("utf-8")
        print(str(answer))
        answer = json.dumps(answer)
        answer = convert_json_protocol(answer.__dict__)
        sock.send(bytes(conf_key))
    except socket.error as msg:
        print("Error trying to connect to socket: "+str(msg))
        print("Retrying...")
        socket_connect()

socket_connect()
