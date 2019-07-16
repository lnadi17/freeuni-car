import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(7,GPIO.OUT)

def update_headlight(data):
	data = data.decode('utf-8').lower()
	index = data.indexOf(' ')
	first word = data.substring(0, index)

	if("headlights" == first word):
		if("true" in data.substring(index))
		GPIO.output(7, GPIO.HIGH)

		else if("false" in data.substring(index)):
			GPIO.output(7, GPIO.LOW)