import RPi.GPIO as GPIO
import time
import math


def setup(rsp=[20,16]):
    global read_speed_pins
    read_speed_pins = [ rsp[0], # left pin
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
    global dis_sensor_holes
    dis_sensor_holes = cercum / holes


def read_speed(values=5, motor=0):
    # vars
    prevstate = 0
    end = 0
    start = time.time()
    duration = 0
    speed = 0
    measured_values = []


    for i in range(values+1):
        while True:
            # take current value
            currentstate = GPIO.input(read_speed_pins[motor])
            
            # if currentstate of pin == 0 & previous state == 1 =>
            # => period has ended
            if (currentstate == 0 and prevstate == 1):
                # timestamp for end of period and beginning of new
                timestp = time.time()
                if (i > 0):
                    # time of period = timestamp from start - timestamp from end
                    end = timestp
                    duration = end-start
                    # speed = distance / duration
                    speed = dis_sensor_holes/duration
                    
                    if (speed < 100):
                        # speed is appended to array
                        measured_values.append(speed)
                        break
                
                # start of period starts when last ended
                start = timestp
                
                # a small delay to remove faulty values
            elif (currentstate == 1 and prevstate == 0):
                prevstate = 1
                break
       
    # return the values measured
    return measured_values

setup()
while True:
    print(read_speed(motor=1))