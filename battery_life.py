import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

r1 = 10000
r2 = 10000
c = (r1 + r2) / r1


def battery_percentage(event, connection):
    while event.is_set():
        message = b'percentage '
        ads = ADS.ADS1115(i2c)
        chan = AnalogIn(ads, ADS.P0)
        battery_voltage = chan.voltage * c
        battery_percentage = str(int((battery_voltage - 7.1) / 0.9 * 100))
        message = message + bytes(battery_percentage, 'utf-8')
        if (int(battery_voltage) == 8):
            message = b'percentage Charging'
        try:
            connection.sendall(message)
        except OSError:
            print("OSError, no problem")
        print(str(battery_percentage) + " and " + str(battery_voltage))
        time.sleep(15)
