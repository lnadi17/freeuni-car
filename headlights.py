import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

def update_headlights(data):
	data = data.decode('utf-8').lower()
	first_word = data.split()[0]

	if ("headlights" == first_word):
		if ("true" in data):
			GPIO.output(7, GPIO.HIGH)
		elif ("false" in data):
			GPIO.output(7, GPIO.LOW)