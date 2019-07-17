import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
tracker_Pin_fwd = 11
tracker_Pin_bcw = 13
GPIO.setup(tracker_Pin_fwd, GPIO.IN)
GPIO.setup(tracker_Pin_bcw, GPIO.IN)

def is_danger_forward(connection):
	message = "tracking"

	if (GPIO.INPUT(tracker_Pin_fwd) == GPIO.LOW):
		boolean = " True"
	else:
		boolean = " False"

	message = message + boolean
	connection.sendall(message)

def is_danger_backward(connection):
	message = "tracking"

	if (GPIO.INPUT(tracker_Pin_bcw) == GPIO.LOW):
		boolean = " True"
	else:
		boolean = " False"

	message = message + boolean
	connection.sendall(message)