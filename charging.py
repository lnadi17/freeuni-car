import RPi.GPIO as GPIO
from numpy import sqrt
from engine import l, r
from time import sleep

l1 = 23
l2 = 24
l_en = 13
lf = 1

r1 = 20
r2 = 21
r_en = 19
rf = 1

turn_time = 1

l.start(0)
r.start(0)

charging_bool = False

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
    global charging_bool
    data = data.decode('utf-8').split()
    if (data[0] == 'charging'):
        if (data[1] == 'true'):
            charging_bool = True
        if (data[1] == 'false'):
            charging_bool = False
    return charging_bool


def get_average_line(line1, line2):
    br = line1[0]
    kr = (line1[1] - line1[0]) / 640
    if(kr == 0):
        kr = 0.1

    bg = line2[0]
    kg = (line2[1] - line2[0]) / 640
    if(kg == 0):
        kg = 0.1

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


def line_rect_inter(y0, k, r_width, r_height):
    y_x_eq_0 = y0
    y_x_eq_wid = k * r_width + y0
    x_y_eq_0 = (0 - y0) / k
    x_y_eq_height = (r_height - y0) / k

    y_x_eq_0_b = False
    y_x_eq_wid_b = False
    x_y_eq_0_b = False
    x_y_eq_height_b = False

    if(y_x_eq_0 >= 0 and y_x_eq_0 <= r_height):
        y_x_eq_0_b = True

    if(y_x_eq_wid >= 0 and y_x_eq_wid <= r_height):
        y_x_eq_wid_b = True

    if(x_y_eq_0 >= 0 and x_y_eq_0 <= r_width):
        x_y_eq_0_b = True

    if(x_y_eq_height >= 0 and x_y_eq_height <= r_width):
        x_y_eq_height_b = True

    x1 = -1
    y1 = -1
    x2 = -1
    y2 = -1

    if(x_y_eq_height_b):
        x1 = x_y_eq_height
        y1 = r_height

    if(x_y_eq_0_b):
        if(x1 == -1):
            x1 = x_y_eq_0
            y1 = 0
        else:
            x2 = x_y_eq_0
            y2 = 0

    if(y_x_eq_wid_b):
        if(x1 == -1):
            x1 = r_width
            y1 = y_x_eq_wid
        else:
            x2 = r_width
            y2 = y_x_eq_wid
    if(y_x_eq_0_b):
        x2 = 0
        y2 = y_x_eq_0

    if(y1 < y2):
        return x2, y2, x1, y1

    return x1, y1, x2, y2


def charge_loop(connection):
    while True:
        connection.sendall(b'line get')

        data = connection.recv(32)

        if not data:
            print("No data")
            break

        if not (is_charging(data)):
            break
        # Parse data
        data = data.decode('utf-8').split()

        if (data[0] != 'line'):
            continue

        if (data[1] == 'no'):
            print("no line data")
            continue

        red_line = list(map(int, data[1].split(",")))
        green_line = list(map(int, data[2].split(",")))

        y0, y1 = get_average_line(red_line, green_line)  # x is considered 640
        k = (y1 - y0) / 640

        x_in1, y_in1, x_in2, y_in2 = line_rect_inter(y0,k,640,480) # intersection points

        print(x_in1, " ", y_in1, " ", x_in2, " ", y_in2)

        if (y_in1 == 480):
                if(x_in2 > 640 * 3 / 4):  # incline forwards
                    left(0.3)
                    forward(0.1)
                    if (x_in1 > 640 * 3 / 4):  # box right

                elif (x_in2 < 640 * 3 / 4 and x_in2 > 640 * 1 / 4):  # go towards
                    left(0.1)
                    forward(0.1)
                else:  # incline towards
                    right(0.3)
                    forward(0.1)
            elif (x_in1 < 640 * 3 / 4 and x_in1 > 640 * 1 / 4):  # middle of the box

                if (x_in2 > 640 * 3 / 4):  # incline forwards
                    right(0.3)
                    forward(0.1)
                elif (x_in2  < 640 * 3 / 4 and x_in2  > 640 * 1 / 4):  # go towards
                    forward(0.1)
                else:  # incline towards
                    left(0.3)
                    forward(0.1)

            else:  # left of box

                if (x_in2 > 640 * 3 / 4):  # incline forwards
                    right(0.3)
                    forward(0.1)

                elif(x_in2  < 640 * 3/4 and x_in2  > 640 * 1/4): # go towards
                    right(0.1)
                    forward(0.1)
                else : # incline towards
                    left(0.3)
                    forward(0.1)

        elif(x_in1 == 0):

            if(x_in2 < 640 * 1 / 4):  # on right side
                left(0.3)
                forward(0.05)
            elif(x_in2 < 640 * 3 / 4 and x_in2 > 640*1 /4):  # make a move bare it
                forward(0.05)
            else(x_in2 > 640 * 3 / 4):  # if forward then cross, so go left
                right(0.2)
                forward(0.05)

        elif(x_in2 == 640):

            if(x_in2 > 640 * 3 / 4):  # on right side
                right(0.3)
                forward(0.05)
            elif(x_in2 < 640 * 3 / 4 and x_in2 > 640* 1 /4):  # make a move bare it
                forward(0.05)
            else(x_in2 < 640 * 1 / 4):  # if forward then cross, so go left
                left(0.2)
                forward(0.05)



    # sleep(10)
