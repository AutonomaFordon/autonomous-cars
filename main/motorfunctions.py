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

def drive(pl=1, pr=1):
    if(pl):
        pacel = fl_num + (100-fl_num)*(pl-1)/5.0
    else:
        pacel = 0
    if(pr):
        pacer = fr_num + (100-fr_num)*(pr-1)/5.0
    else:
        pacer = 0
    
    pwml.ChangeDutyCycle(pacel)
    pwmr.ChangeDutyCycle(pacer)
    GPIO.output(motorr[1], False)
    GPIO.output(motorl[1], False)
    return 1

def calibrate(read_speed_pins=[20,16]):
    print("calibrating")
    max_time=2
    global fl_num
    global fr_num
    fl_num = 15
    fr_num = 15
    lspeed = [0,0,0]
    rspeed = [0,0,0]
    speed.setup(rsp=read_speed_pins)
    
    for i in [8, 2]:
        while(lspeed[2]<2):
            fl_num += i
            pwml.ChangeDutyCycle(fl_num)
            GPIO.output(motorl[1], False)
            lspeed = speed.read_speed(values=3,motor=0,time_lim=max_time)
            print("Left: +"+str(i)+"\nPWM: "+str(fl_num)+"\nSpeed: "+str(lspeed))
            
        while(lspeed[2]>2):
            fl_num -= i/2
            pwml.ChangeDutyCycle(fl_num)
            GPIO.output(motorl[1], False)
            lspeed = speed.read_speed(values=3,motor=0,time_lim=max_time)
            print("Left: -"+str(i/2)+"\nPWM: "+str(fl_num)+"\nSpeed: "+str(lspeed))
    
    while(lspeed[2]>2):
        fl_num += 0.5
        pwml.ChangeDutyCycle(fl_num)
        GPIO.output(motorl[1], False)
        lspeed = speed.read_speed(values=3,motor=0,time_lim=max_time)
        print("Left: -"+"0.5"+"\nPWM: "+str(fl_num)+"\nSpeed: "+str(lspeed))
        
    pwml.ChangeDutyCycle(0)
    
    for i in [8, 2]:
        while(rspeed[2]<2):
            fr_num += i
            pwmr.ChangeDutyCycle(fr_num)
            GPIO.output(motorr[1], False)
            rspeed = speed.read_speed(values=3,motor=1,time_lim=max_time)
            print("Right: +"+str(i)+"\nPWM: "+str(fr_num)+"\nSpeed: "+str(rspeed))
            
        while(rspeed[2]>2):
            fr_num -= i/2
            pwmr.ChangeDutyCycle(fr_num)
            GPIO.output(motorr[1], False)
            rspeed = speed.read_speed(values=3,motor=1,time_lim=max_time)
            print("Right: -"+str(i/2)+"\nPWM: "+str(fr_num)+"\nSpeed: "+str(rspeed))
            
    while(rspeed[2]<2):
        fr_num += 0.5
        pwmr.ChangeDutyCycle(fr_num)
        GPIO.output(motorr[1], False)
        rspeed = speed.read_speed(values=3,motor=1,time_lim=max_time)
        print("Right: -"+"0.5"+"\nPWM: "+str(fr_num)+"\nSpeed: "+str(rspeed))
    
    pwmr.ChangeDutyCycle(0)

setup()