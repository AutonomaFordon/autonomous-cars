import RPi.GPIO as GPIO
import time

analog_pin = [20,	# left pin
			16]		# right pin

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(analog_pin[0], GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(analog_pin[1], GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    print(str(GPIO.input(analog_pin[0])))
    time.sleep(1)