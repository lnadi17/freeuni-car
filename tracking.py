import RPi.GPIO as GPIO

tracker_pin_fwd = 25
tracker_pin_bcw = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(tracker_pin_fwd, GPIO.IN)
GPIO.setup(tracker_pin_bcw, GPIO.IN)

def is_danger_forward(connection):
	message = b'tracking '

	if (GPIO.input(tracker_pin_fwd) == GPIO.LOW):
		print("rame")
		boolean = b'True'
		message = message + boolean
		connection.sendall(message)
		return True
	else:
		boolean = b'False'
		message = message + boolean
		connection.sendall(message)
		return False



def is_danger_backward(connection):
	message = b'tracking '

	if (GPIO.input(tracker_pin_bcw) == GPIO.LOW):
		boolean = b'True'
		message = message + boolean
		connection.sendall(message)
		return True
	else:
		boolean = b'False'
		message = message + boolean
		connection.sendall(message)
		return False
