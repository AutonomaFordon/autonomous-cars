import RPi.GPIO as GPIO
import time
import math


def setup(rsp=[20,16]):
    global read_speed_pins = [rsp[0], # left pin
                              rsp[1]] # right pin
    
    # setup
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # set pins to inputs
    GPIO.setup(read_speed_pins[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(read_speed_pins[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # factors
    holes = 10
    wheel_diameter = 7
    cercum = wheel_diameter * math.pi
    dis_sensor_holes = cercum / holes


def read_speed(values=5, motor=0):
    # vars
    prevstate = 0
    end = 0
    start = time.time()
    duration = 0
    speed = 0


    for i in range(values):
        #time.sleep(0.001)
        # take current value
        currentstate = GPIO.input(analog_pin[0])
        
        # if currentstate of pin == 0 & previous state == 1
        # 
        if (currentstate == 0 and prevstate == 1):
            end = time.time()
            print("end: "+str(time.time()))
            duration = end-start
            speed = dis_sensor_holes/duration
            start = end
            print("start: "+str(time.time()))
            time.sleep(0.02)
        elif (currentstate == 1 and prevstate == 0):
            prevstate = 1
            continue 	# So that the speed doesn't print
        else :
            continue
        print("speed left motor: "+str(speed)+" cm/s")
        print("duration: "+str(duration))
        print("distance: "+str(dis_sensor_holes))
