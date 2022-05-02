import socket
import json

UDP_IP = {
    "birk": "192.168.0.3",
    "sten": "192.168.0.4",
    "kent": "192.168.0.2"
    }

UDP_PORT = 5005
RECIEVER = UDP_IP["kent"]

MESSAGE = {
	"name": "David",
	"age": "18"
	}

json_MESSAGE = json.dumps(MESSAGE)

print(MESSAGE["name"]+" är "+MESSAGE["age"])
print("sent to "+RECIEVER+" via port "+str(UDP_PORT))

sock = socket.socket(socket.AF_INET, #interrupt
			socket.SOCK_DGRAM) #UDP

sock.connect((RECIEVER, UDP_PORT))
sock.sendall(bytes(json_MESSAGE, "utf-8"))
