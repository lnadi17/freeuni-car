import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

def update_headlight(data):
	GPIO.setup(7,GPIO.OUT)

	if(data == "dark"):
		GPIO.output(7, GPIO.HIGH)

	else if(data == "bright"):
		GPIO.output(7, GPIO.LOW)