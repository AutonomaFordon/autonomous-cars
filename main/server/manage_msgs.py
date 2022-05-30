import socket
import json
import sys
sys.path.append("../resources/")
from protocols import *

conns = {}

# static ip:s
UDP_IP = {
    "birk": "192.168.0.3",
    "sten": "192.168.0.4",
    "kent": "192.168.0.2"
    }

# Password
conf_key = "Ghent2021!"

# Protocol object
myProtocol = Protocol("192.168.0.5")

# Creating a socket
def socket_create():
    try:
        global host
        global port
        global sock
        host = "192.168.0.5"
        port = 5006
        sock = socket.socket()
    except socket.error as msg:
        print("Error creating socket: "+str(msg))
        
# Binding to socket
def socket_bind():
    try:
        global host
        global port
        global sock
        print("Binding socket to port: "+str(port))
        sock.bind((host, port))
        sock.listen(5)
    except socket.error as msg:
        print("Error binding to socket: "+str(msg))
        print("Retrying...")
        socket_bind()

# Accepting/refusing connections
def socket_accept():
    conn, address = sock.accept()
    establish_conn, prtc_id = myProtocol.mkptc(rec=address[0], typeof="est_req")
    try:
        respond = send_respond(conn, establish_conn, True)
        respond = respond.decode("utf-8")
        respond = json.loads(respond)
        respond = str(respond)
        # Password has to match
        if (respond == conf_key):
            print("Connection has been established | IP "+address[0]+" | Port "+str(address[1]))
            return conn, address
        else:
            conn.close()
            print("Invalid key from "+address[0])
            return False
    except:
        conn.close()
        print("Invalid respond trying to connect")

# Sending messages to units
def send_respond(conn, protocol, exp_res=False):
    try:
        print(protocol)
        print(bytes(protocol, "utf-8"))
        conn.send(bytes(protocol, "utf-8"))
        print("done")
        # If we are expecting a respond
        if(exp_res):
            respond = conn.recv(1024)
            return respond
        else:
            print("Protocol "+str(protocol.ID)+" succesfully sent")
            return True
    except socket.error as msg:
        print("Error sending: "+str(msg))
        return False

# Waiting for all the cars to connect
def connect_all_cars():
    other_conns=0
    while(len(conns)-other_conns < 3):
        print("Looking for connections")
        prev_len=len(conns)
        try:
            conn, address = socket_accept() # might be error here, since socket_accept() can return 1 value
            for i in UDP_IP:
                if(UDP_IP[i][-1] == address[0][-1]):
                    conns[i] = conn
                    break
            if(len(conns) > prev_len):
                continue
            print("IP "+address[0]+" not one of the cars\nDo you accept the connection?(y/n)")
            accept = input()
            if (accept=="y"):
                other_conns += 1
                conns[str(len(conns))] = conn
            else:
                conn.close()
                print("Connection to "+address[0]+" closed")
        except:
            print("Failed to connect")
    print("All cars connected")

# Closing sockets
def destroy():
    sock.close()
    print("Socket closed")

# Main
def main():
    socket_create()
    socket_bind()
    connect_all_cars()

try:
    main()
except:
    destroy()
