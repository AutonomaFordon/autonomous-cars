import RPi.GPIO as GPIO
import time
import math

analog_pin = [20,	# left pin
			16]		# right pin

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set pins to inputs
GPIO.setup(analog_pin[0], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(analog_pin[1], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# factors
holes = 10
wheel_diameter = 7
cercum = wheel_diameter * math.pi
dis_sensor_holes = cercum / holes

# vars
prevstate = 0
end = 0
start = time.time()
duration = 0
speed = 0

# currentstate == 0 & prevstate == 1 -> 
# -> start = timestamp & prevstate = 0

# currentstate == 1 & prevstate == 0 -> prevstate = 1

# currentstate == 0 & prevstate == 1 -> 
# -> end = timestamp & duration = end - start, start = end

# loop

while True:
    time.sleep(0.001)
# 	for i in range(2): 		# Begin with left motor
# 		for j in range(4): 	# Three measures for each motor,
# 							# first is skipped (will be wrong prbl)
    currentstate = GPIO.input(analog_pin[0])
    if (currentstate == 0 and prevstate == 1):
#         if (j==0):
#             start = time.time()
#             continue
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
