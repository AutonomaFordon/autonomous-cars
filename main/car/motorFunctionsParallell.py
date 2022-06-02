import RPi.GPIO as GPIO
import time
import read_speed as speed

def setup(pins = [[13,5],[12,6]], read_speed_pins=[20,16]):
    
    #Declare global variables
    global motorl 
    global motorr
    
    #Establishing pins for motors
    motorl = pins[0]
    motorr = pins[1]
    
    GPIO.setmode(GPIO.BCM) #Set label type on GPIO pins to GPIO-pin numbers
    GPIO.setwarnings(False) #Disable warning msg in console

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

    #all motor pins set to zero
    GPIO.output(motorl[0], False)
    GPIO.output(motorl[1], False)
    GPIO.output(motorr[0], False)
    GPIO.output(motorr[1], False)
    
    #Setup speed reading sensors
    speed.setup(rsp=read_speed_pins)

#Function used to set speed from main
def setSpeed(curve, speed): 
    
    if(curve > 0):
        pwmr.ChangeDutyCycle(5*speed)
        pwml.ChangeDutyCycle(75*speed)
    elif(curve < 0):
        pwmr.ChangeDutyCycle(75*speed)
        pwml.ChangeDutyCycle(5*speed)
    else:
        pwmr.ChangeDutyCycle(75*speed)
        pwml.ChangeDutyCycle(75*speed)
        
setup()
