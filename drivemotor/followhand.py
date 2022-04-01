import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor

#pins used for motors, first uses pwm, second does not
motorl = [13, 5] #left motor pins
motorr = [12, 6] #right motor pins

#pins for ultrasonicsensor
trig = 4 #triggerpin
ec = 17 #echopin

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)

	#Set all motor pins as output
	GPIO.setup(motorl[0], GPIO.OUT)
	GPIO.setup(motorl[1], GPIO.OUT)
	GPIO.setup(motorr[0], GPIO.OUT)
	GPIO.setup(motorr[1], GPIO.OUT)

	#PWM setup
	global pwml
	global pwmr
	pwml = GPIO.PWM(motorl[0], 1000)
	pwmr = GPIO.PWM(motorr[0], 1000)
	
	#PWM start
	pwml.start(0)
	pwmr.start(0)

	#setup distancesensor, making object ultrasonic
	global ultrasonic
	ultrasonic = DistanceSensor(echo=ec, trigger=trig, max_distance=2.0)

	#all motor pins = 0
	GPIO.output(motorl[0], False)
	GPIO.output(motorl[1], False)
	GPIO.output(motorr[0], False)
	GPIO.output(motorr[1], False)


def loop():
	while True:
		dist = ultrasonic.distance*100
		print(dist)
		if(dist < 40 and dist > 5):
			pace = 100 * (dist-5)/35
		elif(dist>40):
			pace=100
		else:
			pace=0
		pwml.ChangeDutyCycle(pace)
		pwmr.ChangeDutyCycle(pace)
		GPIO.output(motorr[1], False)
		GPIO.output(motorl[1], False)

def sluta():
	GPIO.output(motorl[0], False)
	GPIO.output(motorl[1], False)
	GPIO.output(motorr[0], False)
	GPIO.output(motorr[1], False)

def destroy():
	pwm.stop()
	GPIO.output(ledPin, GPIO.LOW)
	GPIO.cleanup()

setup()
destroy()
