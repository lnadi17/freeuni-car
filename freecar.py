import socket
import time
import os
from engine import *
from find import *
from threading import Thread, Event

SOCKET_PATH='/tmp/uv4l.socket'

find_event = Event()

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
        l_decrease_thread = Thread(target=update_location, args=(find_event, connection,))
        l_decrease_thread.start()

        while True:
            data = connection.recv(16)

            if not data:
                print("No data")
                break;

            print("Received message: %s" % data)
            
            run_engine_with_keyboard_input(data)
            update_headlights(data)

            time.sleep(0.01)
    finally:
        find_event.clear()
        GPIO.cleanup()
        connection.close()

