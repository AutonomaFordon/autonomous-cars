from gpiozero import DistanceSensor
import time

def dis_init(ec=17, trig=4):
	return DistanceSensor(echo=ec, trigger=trig, max_distance=2.0)
	
def get_dis(obj):
	return obj.distance*100

ultra = dis_init()
while True:
    time.sleep(0.5)
    print(get_dis(ultra))
