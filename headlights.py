import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

def update_headlights(data):
	data = data.decode('utf-8').lower()
	index = data.indexOf(' ')
	first_word = data.substring(0, index)

	if ("headlights" == first_word):
		if ("true" in data.substring(index)):
			GPIO.output(7, GPIO.HIGH)
		elif ("false" in data.substring(index)):
			GPIO.output(7, GPIO.LOW)