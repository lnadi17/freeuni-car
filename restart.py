#!/usr/bin/env python3
#coding=utf-8

import time
import pigpio

#setup vars
gpio = 2 #where the switch is connected
debounce = 1000 #debounce time, in us
clickPeriod = 5000 #control period for clicks. in ms
clickCount = -1 #number of clicks in the period

def intCallback(g, level, tick):
	global clickCount
	if level == pigpio.HIGH:
		#button release
		if clickCount == -1:
			#this is the starting click. Setting up watchdog
			pi.set_watchdog(g, clickPeriod)
		clickCount += 1
	elif level == pigpio.TIMEOUT:
		#kill watchdog and print result
		pi.set_watchdog(g, 0)
		print("Total clicks in {}ms period: {}".format(clickPeriod, clickCount)
		clickCount = -1

pi = pigpio.pi()
pi.set_mode(gpio, pigpio.INPUT)
pi.set_glitch_filter(gpio, debounce)
pi.set_pull_up_down(gpio, pigpio.PUD_UP) #this depends on how the switch is connected. In this case it is between GPIO and GND
cb = pi.callback(gpio, pigpio.RISING_EDGE, intCallback)

try:
	while True:
		time.sleep(1)

except (KeyboardInterrupt, SystemExit) as e:
	print("Clean exit")

except Exception as e:
	print("Bad exit")

finally:
	cb.cancel()
	pi.stop()
