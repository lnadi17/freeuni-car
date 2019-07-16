import subprocess
from time import sleep
from threading import Event

def update_location(event, connection):
	while (event.is_set()):
		try:
			result = subprocess.run(['sudo', '/home/pi/Desktop/webcar/fingerprint', '-g', 'eng', '-s', 'http://192.168.98.17:8003', '-c', '1', '--nodebug'], stdout=subprocess.PIPE)
			if (result):
				connection.sendall(b'location ' + result.stdout)
		except:
			connection.sendall(b'location unknown')
		sleep(1)