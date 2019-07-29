import RPi.GPIO as GPIO
from engine import stop_engine
import time


def is_danger_forward(event, connection):
    while (event.is_set()):
        dist = distance(event)
        message = b'tracking '
        if (event.is_set()):
            if (dist > 13):
                stop_engine()
                boolean = b'True'
                message = message + boolean
                connection.sendall(message)
            else:
                boolean = b'False'
                message = message + boolean
                connection.sendall(message)
            time.sleep(0.01)


def distance(event):
    # set Trigger to HIGH
    GPIO.output(18, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(18, False)

    start_time = time.time()
    stop_time = time.time()

    # Save start time
    start_time_t = start_time
    try:
        while (event.is_set() and GPIO.input(17) == 0):
            start_time = time.time()
            if (start_time - start_time_t > 0.1):
                # print("entered start time loop")
                return -1

        # Save time of arrival
        stop_time_t = start_time
        while (event.is_set() and GPIO.input(17) == 1):
            stop_time = time.time()
            if (stop_time - stop_time_t > 0.1):
                # print("entered stop time loop")
                return -1
    except RuntimeError:
        print("Runtime error, exiting")
        exit()

    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2
    return distance
