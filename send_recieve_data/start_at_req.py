import communication as comm
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)

SENDER="birk"
RECIEVERR="birk"



comm.send_data(RCVR=RECIEVERR, MESSAGE={"type":"hs_req",
                                       "sender":SENDER,
                                       "nxt_type":"start_time",
                                       "reciever":RECIEVERR})
print("1")
answer={}
answer=comm.recieve_data(TYPE="hs_res")
print("2")
when=time.time()+2

comm.send_data(RCVR=RECIEVERR, MESSAGE={"type":"start_time",
                                        "sender":SENDER,
                                        "time":str(when),
                                        "reciever":RECIEVERR})
print("3")
while True:
    print(time.time())
    print(when)
    if(int(time.time())>int(when)):
        GPIO.output(23, True)
        break