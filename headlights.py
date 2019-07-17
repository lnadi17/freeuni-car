import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

def update_headlights(data):
	data = data.decode('utf-8').lower()
	first_word = data.split()[0]

	if ("headlights" == first_word):
		print("headlights")
		if ("true" in data):
			GPIO.output(4, GPIO.HIGH)
		elif ("false" in data):
			GPIO.output(4, GPIO.LOW)