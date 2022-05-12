import socket
import json
import time

UDP_IP = {
    "birk": "192.168.0.3",
    "sten": "192.168.0.4",
    "kent": "192.168.0.2"
    }

UDP_PORT = 5005

def send_data(RCVR="birk", MESSAGE= {"name": "David","age": "18"}):
	
	json_MESSAGE = json.dumps(MESSAGE)
	
	RECIEVER = UDP_IP[RCVR]
	
	sock = socket.socket(socket.AF_INET, #interrupt
					socket.SOCK_DGRAM) #UDP
	sock.connect((RECIEVER, UDP_PORT))
	
	sock.sendall(bytes(json_MESSAGE, "utf-8"))

	sock = socket.socket(socket.AF_INET, #interrupt
				socket.SOCK_DGRAM) #UDP

	sock.connect((RECIEVER, UDP_PORT))
	sock.sendall(bytes(json_MESSAGE, "utf-8"))
	
	sock.close()

def recieve_data(TYPE="hs_res"):
	sock = socket.socket(socket.AF_INET, #internet
					socket.SOCK_DGRAM) #UDP
	print("ja")
	sock.bind((UDP_IP["sten"], UDP_PORT))
	
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 byte
		
		data = data.decode("utf-8")
		data = json.loads(data)
		print("hej")
		
		if(data["type"]==TYPE):
			break
	sock.close()
	
	return data
	
