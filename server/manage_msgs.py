import socket
import sys
sys.path.append("../resources/")
import protocols

UDP_IP = {
    "birk": "192.168.0.3",
    "sten": "192.168.0.4",
    "kent": "192.168.0.2"
    }

conf_key = "Ghent2021"

def socket_create():
    try:
        global host
        global port
        global sock
        host = ''
        port = 5005
        sock = socket.socket(socket.AF_INET, #interrupt
                            socket.SOCK_DGRAM) #UDP
    except socket.error as msg:
        print("Error creating socket: "+str(msg))
        
def socket_bind():
    try:
        global host
        global port
        global s
        print("Binding socket to port: "+str(port))
        s.bind((host, port))
        s.listen(5)
    except socket.error as msg:
        print("Error binding to socket: "+str(msg))
        print("Retrying...")
        socket_bind()
    
def socket_accept():
    conn, address = s.accept()
    print("Connection has been established | IP "+address[0]+" | Port "+str(address[1]))
    establish_conn = hs_req(sender=host, reciever=address[0], nxt_action="establish_conn", ID=0)
    send(conn, hs_req)

def send(conn, protocol):
    try:
        conn.sendall(protocol)
    except socket.error as msg:
        print("Error sending: "+str(msg))

def main():
    socket_create()
    socket_bind()
    socket_accept()