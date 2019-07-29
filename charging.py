import RPi.GPIO as GPIO
from numpy import sqrt
from time import sleep

charging = False

l1 = 23
l2 = 24
l_en = 13
lf = 1

r1 = 20
r2 = 21
r_en = 19
rf = 1

l = GPIO.PWM(l_en, 1000)
r = GPIO.PWM(r_en, 1000)

turn_time = 1

l.start(0)
r.start(0)


def stop():
    l.ChangeDutyCycle(0)
    r.ChangeDutyCycle(0)


def start():
    l.ChangeDutyCycle(50)
    r.ChangeDutyCycle(50)


def forward(time):
    GPIO.output(l1, GPIO.HIGH)
    GPIO.output(l2, GPIO.LOW)
    GPIO.output(r1, GPIO.HIGH)
    GPIO.output(r2, GPIO.LOW)
    start()
    sleep(time)
    stop()


def left(time):
    GPIO.output(l1, GPIO.LOW)
    GPIO.output(l2, GPIO.HIGH)
    GPIO.output(r1, GPIO.HIGH)
    GPIO.output(r2, GPIO.LOW)
    start()
    sleep(time)
    stop()


def right(time):
    GPIO.output(l1, GPIO.HIGH)
    GPIO.output(l2, GPIO.LOW)
    GPIO.output(r1, GPIO.LOW)
    GPIO.output(r2, GPIO.HIGH)
    start()
    sleep(time)
    stop()


def backward(time):
    GPIO.output(l1, GPIO.LOW)
    GPIO.output(l2, GPIO.HIGH)
    GPIO.output(r1, GPIO.LOW)
    GPIO.output(r2, GPIO.HIGH)
    start()
    sleep(time)
    stop()


def is_charging(data):
    global charging

    data = data.decode('utf-8').split()

    if (data[0] == 'charging'):
        if (data[1] == 'true'):
            charging = True
        if (data[1] == 'false'):
            charging = False

    return charging


def get_average_line(line1, line2):
    br = line1[0]
    kr = (line1[1] - line1[0]) / 640

    bg = line2[0]
    kg = (line2[1] - line2[0]) / 640

    alpha = (kr + kg) / (1 - kr * kg)
    k_avg = (sqrt(1 + alpha * alpha) - 1) / alpha

    intersection_x = (bg - br) / (kr - kg)
    intersection_y = kr * intersection_x + br
    b_avg = intersection_y - k_avg * intersection_x

    # Turn the line if neccessary
    dy = 1
    xrf = (intersection_y + dy - br) / kr
    xgf = (intersection_y + dy - bg) / kg
    xbf = (intersection_y + dy - b_avg) / k_avg

    if ((xbf < xrf and xbf < xgf) or (xbf > xrf and xbf > xgf)):
        k_avg = - 1 / k_avg
        b_avg = intersection_y - k_avg * intersection_x

    y0 = int(b_avg)
    y1 = int(k_avg * 640 + b_avg)

    return y0, y1


def follow_lines(data):
    # Parse data
    data = data.decode('utf-8').split()

    if (data[0] is not 'line'):
        print("No line data")
        break

    if (data[1] is 'no'):
        break

    # y0, y1 = get_average_line([green_line, red_line]) # x is considered 640
