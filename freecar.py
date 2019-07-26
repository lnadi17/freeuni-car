import socket
import time
import os
from engine import *
from find import *
from tracking import *
from threading import Thread, Event
from headlights import *
# from battery_life import *

SOCKET_PATH='/tmp/uv4l.socket'

find_event = Event()
danger_event = Event()

try:
    os.unlink(SOCKET_PATH)
except OSError:
    if os.path.exists(SOCKET_PATH):
        raise

s = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)

print("SOCKET_PATH: %s" % SOCKET_PATH)
s.bind(SOCKET_PATH)
s.listen(1)

while True:
    print("Awaiting connection...")
    connection, client = s.accept()

    try:
        print("Established connection.")
        gpio_setup()

        find_event.set()
        danger_event.set()

        location_thread = Thread(target=update_location, args=(find_event, connection,))
        location_thread.start()

        danger_thread_foward = Thread(target=is_danger_forward, args=(danger_event, connection,))
        danger_thread_foward.start()

        # battery_thread = Thread(target=battery_percentage, args=(connection,))
        # battery_thread.start()

        while True:
            data = connection.recv(16)

            if not data:
                print("No data")
                break;

            print("Received message: %s" % data)
            update_headlights(data)
            run_engine_with_keyboard_input(data)
            time.sleep(0.01)
    finally:
        find_event.clear()
        danger_event.clear()
        GPIO.cleanup()
        connection.close()
