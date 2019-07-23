import RPi.GPIO as GPIO
from engine import *
import time

tracker_pin_fwd = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(tracker_pin_fwd, GPIO.IN)



def is_danger_forward(connection):
	while True:
		message = b'tracking '
		dist = distance()
		if (dist > 13):
			print("Measured  Distance = %.1f cm" % dist)
			stop_engine()
			boolean = b'True'
			message = message + boolean
			connection.sendall(message)
		else:
			boolean = b'False'
			message = message + boolean
			connection.sendall(message)
		time.sleep(0.01)




GPIO_TRIGGER = 18
GPIO_ECHO = 2

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    # set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

	StartTime = time.time()
	startTm = StartTime
	StopTime = time.time()
	stopTm = StartTime


	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		 StartTime = time.time()
		 if(StartTime - startTm	 > 0.1):
			 stopTm = StartTime
			 return -7

    # save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()
		if(StopTime - stopTm > 0.1):
			GPIO.output(GPIO_TRIGGER, True)
			break


    # time difference between start and arrival
	TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2

	return distance
