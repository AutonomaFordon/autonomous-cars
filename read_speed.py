import RPi.GPIO as GPIO
import time
import math

analog_pin = [13,	# left pin
			12]		# right pin

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set pins to inputs
GPIO.setup(analog_pin[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(analog_pin[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)

# factors
wheel_diameter = 3
cercum = wheel_diameter * math.pi
dis_sensor_holes = cercum / 10

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
	for i in range(2): 		# Begin with left motor
		for j in range(4): 	# Three measures for each motor,
							# first is skipped (will be wrong prbl)
			currentstate = GPIO.input(analog_pin[i])
			if (currentstate == 0 and prevstate == 1):
				if (j==0): continue
				end = time.time()
				duration = end-start
				speed = dis_sensor_holes/duration
				start = time.time()
			elif (currentstate == 1 and prevstate == 0):
				prevstate = 1
				continue 	# So that the speed doesn't print
			print("speed left motor: "+speed+" m/s")
