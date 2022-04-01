from distance import *

ultrasonic = dis_init(ec=17, trig=4) #init returnerar ultrasonic-objekt

while True:
	print(get_dis(ultrasonic))
