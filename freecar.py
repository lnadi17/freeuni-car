import socket
import time
import os
from engine import *

SOCKET_PATH='/tmp/uv4l.socket'

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
        while True:
            data = connection.recv(16)

            if not data:
                print("No data")
                break;

            print("Received message: %s" % data)
            
            run_engine_with_keyboard_input(data)

            time.sleep(0.01)

    finally:
        GPIO.cleanup()
        connection.close()

