import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import read_speed as speed

def setup(pins = [[13,5],[12,6]]):
    #Establishing pins for motors
    global motorl
    global motorr
    motorl = pins[0]
    motorr = pins[1]
    
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

    #all motor pins = 0
    GPIO.output(motorl[0], False)
    GPIO.output(motorl[1], False)
    GPIO.output(motorr[0], False)
    GPIO.output(motorr[1], False)
    
    #Establishing uncalibrated speed variables
    global fr_num
    global fl_num
    fr_num = 50
    fl_num = 50

def drive(motor=2, pace=1):
    #0 -> left motor, 1 -> right, 2 -> both
    if(pace):
        pacel = fl_num + (100-fl_num)*(pace-1)/5
        pacer = fr_num + (100-fr_num)*(pace-1)/5
    else:
        return 0
    if (motor == 2):
        pwml.ChangeDutyCycle(pacel)
        pwmr.ChangeDutyCycle(pacer)
        GPIO.output(motorr[1], False)
        GPIO.output(motorl[1], False)
    elif (motor == 0):
        pwml.ChangeDutyCycle(pacel)
        GPIO.output(motorl[1], False)
    elif (motor == 1):
        pwmr.ChangeDutyCycle(pacer)
        GPIO.output(motorr[1], False)
    return 1

def calibrate(read_speed_pins=[20,16]):
    print("calibrating")
    fl_num = 40
    fr_num = 20
    lspeed = [0,0,0]
    rspeed = [0,0,0]
    speed.setup(rsp=read_speed_pins)
    while(rspeed[2]<0.5):
        pwmr.ChangeDutyCycle(fr_num)
        GPIO.output(motorr[1], False)
        rspeed = speed.read_speed(values=3,motor=1,time_lim=4)
        fr_num += 4
        print(rspeed)
    while(lspeed[2]<0.5):
        pwml.ChangeDutyCycle(fl_num)
        GPIO.output(motorl[1], False)
        lspeed = speed.read_speed(values=3,motor=0,time_lim=2000)
        fl_num += 8
        print(lspeed)

setup()
calibrate()
print(fl_num)
print(fr_num)
