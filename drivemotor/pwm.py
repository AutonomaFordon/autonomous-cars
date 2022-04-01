import RPi.GPIO as GPIO
import time
 
ledPin = 33
 
def setup():
    global pwm
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledPin, GPIO.OUT)
    GPIO.output(ledPin, GPIO.LOW)
    pwm = GPIO.PWM(ledPin, 1000)
    pwm.start(0)

def loop():
    while True:
        for dc in range(0, 101, 1):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.01)
        time.sleep(1)
        for dc in range(100, -1, -1):
            pwm.ChangeDutyCycle(dc)
            time.sleep(0.01)
        time.sleep(1)

def destroy():
    pwm.stop()
    GPIO.output(ledPin, GPIO.LOW)
    GPIO.cleanup()

setup()
destroy()
