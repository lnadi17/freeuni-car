import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

i2c = busio.I2C(board.SCL, board.SDA)

r1 = 10000
r2 = 10000
c = (r1 + r2) / r1


def battery_percentage(connection):
    while True:
        message = b'percentage '
        ads = ADS.ADS1115(i2c)
        chan = AnalogIn(ads, ADS.P0)
        battery_voltage = chan.voltage * c
        battery_percentage = int((battery_voltage - 7.1) / 1.1 * 100)
        battery_percentage = "%.3f" % battery_percentage
        message = message + bytes(battery_percentage, 'utf-8')
        connection.sendall(message)
        print(str(battery_percentage) + " and " + str(battery_voltage))
        time.sleep(60)
