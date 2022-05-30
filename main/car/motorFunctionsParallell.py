import RPi.GPIO as GPIO
import time
import read_speed as speed

speed_l = 0 #Left motor speed 
speed_r = 0 #Right motor speed

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
def setSpeed(left=0, right=0): 
    #Declare global variables
    global speed_l
    global speed_r
    
    #Update global variables
    speed_l = left
    speed_r = right

    
def trackSpeed(): #Continuously tracks the motors speed and adjust to keep at set value global speed value
    #Declare global variables
    global speed_l
    global speed_r
    
    max_time = 0.2 #Max time before timeout, timeout results in speed as
    
    #Set start value for PWM-signal
    pwm_l = 50
    pwm_r = 50
    
    while(True):
        if(speed_r==0): #If right speed is 0 - turn of left right motor
            pwmr.ChangeDutyCycle(0)
        else: 
            pwm_r = upadateSpeed(pwm_r, speed.read_speed(values=2,motor=1,time_lim=max_time)[1], speed_r) #Read current speed and increase/decrease pwm depending on if current speed is greater or less than set speed
            pwmr.ChangeDutyCycle(pwm_r) #Update motor setting to new PWM-signal
            
            
        if(speed_l==0): #If left speed is 0 - turn of left left motor
            pwml.ChangeDutyCycle(0)
        else:
            pwm_l = upadateSpeed(pwm_l, speed.read_speed(values=2,motor=0,time_lim=max_time)[1], speed_l) #Read current speed and increase/decrease pwm depending on if current speed is greater or less than set speed
            pwml.ChangeDutyCycle(pwm_l) #Update motor setting to new PWM-signal
            
            
def upadateSpeed(pwm_in, speed_in, target_speed): #Updates the pwm
    if(speed_in==0):
        pwm_out = pwm_in + 15   # if the wheel isn't turning it needs a high
                                # PWM-signal to start and should therefor increase
                                # more than if it is moving
    else:
        # if there is a large differense between target and current speed a larger
        # change is needed. The change in the PWM-signal is determined using the
        # difference between target och current speed and multiplying it by 0.1 
        pwm_out = pwm_in + (target_speed - speed_in)*0.1

    # The PWM signal has to be within the interval: 0 <= PWM <= 100
    if(pwm_out<0):
        pwm_out = 0 
    if(pwm_out>100):
        pwm_out=100

    print(speed_in)
    return pwm_out


setup()
