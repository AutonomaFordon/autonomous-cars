import RPi.GPIO as GPIO
import time
import read_speed as speed

speed_l = 0 #Left motor speed 
speed_r = 0 #Right motor speed

def setup(pins = [[13,5],[12,6]], read_speed_pins=[20,16]):
    
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
    
    #Setup speed reading sensors
    speed.setup(rsp=read_speed_pins)

#Function used to set speed from main
def setSpeed(left=0, right=0): 
    global speed_l #Define 
    global speed_r
    
    speed_l = left
    speed_r = right

    
def trackSpeed():
    global speed_l
    global speed_r
    
    max_time = 0.2
    
    pwm_l = 50
    pwm_r = 50
    
    while(True):
        if(speed_r==0):
            pwmr.ChangeDutyCycle(0)
        else:
            pwm_r = upadateSpeed(pwm_r, speed.read_speed(values=2,motor=1,time_lim=max_time)[1], speed_r)
            pwmr.ChangeDutyCycle(pwm_r)
            
            
        if(speed_l==0):
            pwml.ChangeDutyCycle(0)
        else:
            pwm_l = upadateSpeed(pwm_l, speed.read_speed(values=2,motor=0,time_lim=max_time)[1], speed_l)
            pwml.ChangeDutyCycle(pwm_l)
        
        #print("PWM_R =" + str(pwm_r) + "      PWM_L = " + str(pwm_l))
            
            
def upadateSpeed(pwm_in, speed_in, target_speed):
    if(speed_in==0):
        pwm_out = pwm_in + 15
    else:
        pwm_out = pwm_in + (target_speed - speed_in)*0.1
     
    if(pwm_out<0):
        pwm_out = 0
    if(pwm_out>100):
        pwm_out=100

    print(speed_in)
    return pwm_out


setup()