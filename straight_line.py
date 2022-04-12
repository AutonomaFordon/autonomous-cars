import read_speed as rspeed
import RPi.GPIO as GPIO
import time

#pins used for motors, first uses pwm, second does not
motorl = [13, 5] #left motor pins
motorr = [12, 6] #right motor pins

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
	#global ultrasonic
	#ultrasonic = DistanceSensor(echo=ec, trigger=trig, max_distance=2.0)

	#all motor pins = 0
	GPIO.output(motorl[0], False)
	GPIO.output(motorl[1], False)
	GPIO.output(motorr[0], False)
	GPIO.output(motorr[1], False)

def destroy():
	pwml.stop()
	pwmr.stop()
	GPIO.output(motorl[0], GPIO.LOW)
	GPIO.output(motorr[0], GPIO.LOW)
	GPIO.cleanup()

def loop():
	pacel, pacer = 30, 30
	while True:
		pwml.ChangeDutyCycle(pacel)
		GPIO.output(motorl[1], False)
		pwmr.ChangeDutyCycle(pacer)
		GPIO.output(motorr[1], False)
		# set both to a certain speed
		time.sleep(0.5)
		lms=rspeed.read_speed(values=1, motor=0)[0]
		rms=rspeed.read_speed(values=1, motor=1)[0]
		if(lms<rms-2):
			pacel+=2
		elif(rms<lms-2):
			pacer+=2
		else:
			break
	while True:
		print("done")

setup()
rspeed.setup()
loop()
