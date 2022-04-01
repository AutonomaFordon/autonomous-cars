import socket

UDP_IP = {
    "birk": "192.168.0.3",
    "sten": "192.168.0.4",
    "kent": "192.168.0.2"
    }

UDP_PORT = 5005
RECIEVER = UDP_IP["kent"]

MESSAGE = {
	"name": "David",
	"age": 18,
	}

print(MESSAGE["name"]+" är "+MESSAGE["age"]
print("sent to "+RECIEVER+" via port "+UDP_PORT)

sock = socket.socket(socket.AF_INET, #interrupt
			socket.SOCK_DGRAM) #UDP


sock.sendto(MESSAGE, (RECIEVER, UDP_PORT))
