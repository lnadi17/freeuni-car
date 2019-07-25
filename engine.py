import RPi.GPIO as GPIO          
from time import sleep
from threading import Thread, Event

MAX_POWER = 100
NORMAL_POWER = 50
power = NORMAL_POWER

SLEEP_TIME = 0.01 # seconds (for power=50 and SLEEP_TIME=0.02 it lasts for 0.02*50=1 seconds)

l1 = 23
l2 = 24
l_en = 13
lf = 1

r1 = 20
r2 = 21
r_en = 19
rf = 1

print("\n")
print("The default speed & direction of motor is 0 & Forward.")
print("'w/s/a/d' = up/down/left/right; '+/-' = keydown/keyup; ^ = increase/decrease speed")
print("\n")

last_l = 0
last_r = 0

# They're needed when user first presses 'a' and then 'w'
l_swerving = False;
r_swerving = False;

l_is_running = Event()
r_is_running = Event()

def gpio_setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(l1,GPIO.OUT)
    GPIO.setup(l2,GPIO.OUT)
    GPIO.setup(l_en,GPIO.OUT)

    GPIO.output(l1,GPIO.LOW)
    GPIO.output(l2,GPIO.LOW)

    GPIO.setup(r1,GPIO.OUT)
    GPIO.setup(r2,GPIO.OUT)
    GPIO.setup(r_en,GPIO.OUT)

    GPIO.output(r1,GPIO.LOW)
    GPIO.output(r2,GPIO.LOW)

    # Headlights
    GPIO.setup(4,GPIO.OUT)

gpio_setup()

l=GPIO.PWM(l_en,1000)
r=GPIO.PWM(r_en,1000)

l.start(0)
r.start(0)

# Changes power of left wheel and saves its value
def change_left(power):
    global last_l
    last_l = power
    l.ChangeDutyCycle(power)

# Changes power of right wheel and saves its value
def change_right(power):
    global last_r
    last_r = power
    r.ChangeDutyCycle(power)

def l_decrease(run_event):
    current_power = last_l
    while(run_event.is_set()):
        current_power -= 1
        if not current_power < 0:
            l.ChangeDutyCycle(current_power)
        sleep(SLEEP_TIME)
        
def r_decrease(run_event):
    current_power = last_r
    while(run_event.is_set()):
        current_power -= 1
        if not current_power < 0:
            r.ChangeDutyCycle(current_power)
        sleep(SLEEP_TIME) 

def parse_keyboard_input(input):
    input = input.decode('utf-8')
    return input[0], (input[1] == '+')

def run_engine_with_keyboard_input(input):
    global l_swerving
    global r_swerving

    global l_is_running
    global r_is_running

    global power
    
    # Direction is a string, key_pressed is a boolean
    direction, key_pressed = parse_keyboard_input(input)

    if (direction == '^' and key_pressed):
        if (power == MAX_POWER):
            power = NORMAL_POWER
        else:
            power = MAX_POWER

    if (direction == 'w'):
        if (key_pressed):
            # Start moving
            if not l_swerving:
                change_left(power)
            else:
                change_left(0)

            if not r_swerving:
                change_right(power)
            else:
                change_right(0)
            # Forwards
            GPIO.output(l1, GPIO.HIGH)
            GPIO.output(l2, GPIO.LOW)
            GPIO.output(r1, GPIO.HIGH)
            GPIO.output(r2, GPIO.LOW)
        else:
            # Stop moving
            l_is_running.clear()
            r_is_running.clear()
            change_left(0)
            change_right(0)
    elif (direction == 'a'):
        if (key_pressed):
            l_swerving = True
            l_is_running.set()
            l_decrease_thread = Thread(target=l_decrease, args=(l_is_running,))
            l_decrease_thread.start()
        else:
            l_swerving = False
            l_is_running.clear()
            l.ChangeDutyCycle(last_l)
    elif (direction == 's'):
        if (key_pressed):
            # Start moving
            if not l_swerving:
                change_left(power)
            else:
                change_left(0)

            if not r_swerving:
                change_right(power)
            else:
                change_right(0)
            # Backwards
            GPIO.output(l1, GPIO.LOW)
            GPIO.output(l2, GPIO.HIGH)
            GPIO.output(r1, GPIO.LOW)
            GPIO.output(r2, GPIO.HIGH)
        else:
            # Stop moving
            l_is_running.clear()
            r_is_running.clear()
            change_left(0)
            change_right(0)
    elif (direction == 'd'):
        if (key_pressed):
            r_swerving = True
            r_is_running.set()
            r_decrease_thread = Thread(target=r_decrease, args=(r_is_running,))
            r_decrease_thread.start()
        else:
            r_swerving = False
            r_is_running.clear()
            r.ChangeDutyCycle(last_r)

# freezes car in place
def stop_engine():
    GPIO.output(l1, GPIO.LOW)
    GPIO.output(l2, GPIO.LOW)
    GPIO.output(r1, GPIO.LOW)
    GPIO.output(r2, GPIO.LOW)
    l_is_running.clear()
    r_is_running.clear()
    change_left(0)
    change_right(0)