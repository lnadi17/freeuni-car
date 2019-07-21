import RPi.GPIO as GPIO
from engine import *
import time

tracker_pin_fwd = 25
tracker_pin_bcw = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(tracker_pin_fwd, GPIO.IN)
GPIO.setup(tracker_pin_bcw, GPIO.IN)


def is_danger_forward(connection):
	while True:
		message = b'tracking '
		if (GPIO.input(tracker_pin_fwd) == GPIO.LOW):
			stop_engine()
			boolean = b'True'
			message = message + boolean
			connection.sendall(message)
		else:
			boolean = b'False'
			message = message + boolean
			connection.sendall(message)
		time.sleep(0.01)


def is_danger_backward(connection):
	while True:
		message = b'tracking '
		if (GPIO.input(tracker_pin_bcw) == GPIO.LOW):
			stop_engine()
			boolean = b'True'
			message = message + boolean
			connection.sendall(message)
		else:
			boolean = b'False'
			message = message + boolean
			connection.sendall(message)
		time.sleep(0.01)
