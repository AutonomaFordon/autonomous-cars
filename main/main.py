import motorfunctions as motor
import time

motor.calibrate()
time.sleep(2)

motor.drive(2, 2)

input()