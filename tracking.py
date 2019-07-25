import RPi.GPIO as GPIO
from engine import *
import time

def is_danger_forward(connection):
	while True:
		dist = distance()
		message = b'tracking '
		if (dist > 13):
			stop_engine()
			boolean = b'True'
			message = message + boolean
			connection.sendall(message)
		else:
			boolean = b'False'
			message = message + boolean
			connection.sendall(message)
		time.sleep(0.01)

def distance():
    # set Trigger to HIGH
	GPIO.output(18, True)

	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	GPIO.output(18, False)

	start_time = time.time()
	start_time_t = start_time

	stop_time = time.time()
	stop_time_t = start_time

	# Save start time
	while GPIO.input(2) == 0:
		 start_time = time.time()
		 if (start_time - start_time_t > 0.1):
			# stop_time_t = start_time
			return -1

    # Save time of arrival
	while GPIO.input(2) == 1:
		stop_time = time.time()
		if (stop_time - start_time > 0.1):
			# GPIO.output(18, True)
			break

    # time difference between start and arrival
	time_elapsed = stop_time - start_time
	distance = (time_elapsed * 34300) / 2

	return distance
