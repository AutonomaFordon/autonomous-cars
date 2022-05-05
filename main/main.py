import LaneDetection
import RPi.GPIO as GPIO


#pins used for motors, first uses pwm, second does not
motorl = [13, 5] #left motor pins
motorr = [12, 6] #right motor pins

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Set all motor pins as output
GPIO.setup(motorl[0], GPIO.OUT)
GPIO.setup(motorl[1], GPIO.OUT)
GPIO.setup(motorr[0], GPIO.OUT)
GPIO.setup(motorr[1], GPIO.OUT)

#PWM setup
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

while True:

    #Get steering direction
    direction = LaneDetection.steering_dir()

    pace_l = 40
    pace_r = 40

    if(direction>0):
        pace_l += direction*70
        pace_r -= direction*70
        
    if(direction<0):
        pace_l -= abs(direction*100)
        pace_r += abs(direction*100)
        
    pwml.ChangeDutyCycle(pace_l)
    GPIO.output(motorl[1], False)
    pwmr.ChangeDutyCycle(pace_r)
    GPIO.output(motorr[1], False)

    print("Pace")
    print(pace_l)
    print(pace_r)
