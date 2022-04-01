import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motorl = [13, 5] #first pin PWM, second normal GPIO
motorr = [12, 6] #-||-

GPIO.setup(motorl[0],GPIO.OUT)
GPIO.setup(motorl[1],GPIO.OUT)
GPIO.setup(motorr[0],GPIO.OUT)
GPIO.setup(motorr[1],GPIO.OUT)

while True:
	GPIO.output(motorr[0],1)
	GPIO.output(motorr[1],0)

	time.sleep(2)

	GPIO.output(motorr[0],0)
	GPIO.output(motorr[1],1)
	
	time.sleep(2)
	
	GPIO.output(motorr[0],0)
	GPIO.output(motorr[1],0)
	
	time.sleep(2)
