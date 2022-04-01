import socket

UDP_IP = "192.168.0.2" # suppose to be the recievers IP
UDP_PORT = 5005


sock = socket.socket(socket.AF_INET, #internet
			socket.SOCK_DGRAM) #UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024) # buffer size is 1024 byte
	print("recieved message: %s" % data)
