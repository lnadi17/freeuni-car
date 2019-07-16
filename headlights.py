import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)

def update_headlights(data):
	data = data.decode('utf-8').lower()
	first_word = data.split()[0]

	if ("headlights" == first_word):
<<<<<<< HEAD
		if ("true" in data):
			GPIO.output(7, GPIO.HIGH)
		else if ("false" in data):
=======
		if ("true" in data.substring(index)):
			GPIO.output(7, GPIO.HIGH)
		elif ("false" in data.substring(index)):
>>>>>>> d375052165541f78ca715f58db8167c71978b8bd
			GPIO.output(7, GPIO.LOW)