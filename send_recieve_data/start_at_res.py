import communication as comm
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(24, GPIO.OUT)
GPIO.output(24, False)

SENDER="birk"
RECIEVERR="birk"

print("11")
answer={}
answer=comm.recieve_data(TYPE="hs_req")
print("1")

comm.send_data(RCVR=RECIEVERR, MESSAGE={"type":"hs_res",
                                       "sender":SENDER,
                                       "res":"true",
                                       "reciever":RECIEVERR})
print("2")
final=comm.recieve_data(TYPE=answer["nxt_type"])
print("3")
while True:
    print(time.time())
    print(int(float(final["time"])))
    if(int(time.time())>int(float(final["time"]))):
        GPIO.output(24, True)
		break
