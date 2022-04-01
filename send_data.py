import socket

UDP_IP = {
    "birk": "192.168.0.3",
    "sten": "192.168.0.4",
    "kent": "192.168.0.2"
    }

UDP_PORT = 5005
MESSAGE = b"HELLO WORLD!"


RECIEVER = UDP_IP["kent"]

print("UDP target IP: %s" % RECIEVER)
print("UDP target port: %s" % UDP_PORT)
print("message: %s" % MESSAGE)

sock = socket.socket(socket.AF_INET, #interrupt
			socket.SOCK_DGRAM) #UDP
sock.sendto(MESSAGE, (RECIEVER, UDP_PORT))
