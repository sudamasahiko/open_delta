import sys, threading
from time import sleep
#import RPi.GPIO as GPIO
import pigpio

pi = pigpio.pi()

# pins
PIN_DIR_MOT1 = 27
PIN_STEP_MOT1 = 17
PIN_DIR_MOT2 = 10
PIN_STEP_MOT2 = 22
PIN_DIR_MOT3 = 13
PIN_STEP_MOT3 = 6

# NEMA17
# STEP_RESOLUTION = 16 # MODE pins are all HIGH
STEP_RESOLUTION = 8 # HHL
DEG_PER_STEP = 1.8 / STEP_RESOLUTION
DELAY_PER_STEP = 0.012
# DELAY_PER_STEP = 0.006 # 100RPM
# DELAY_PER_STEP = 0.

# other constants
SPR = 360 / DEG_PER_STEP
CW = 1
CCW = 0

# parameter check
def arg_to_steps(arg):
    raw_angle = float(arg)
    if raw_angle == None:
        raw_angle = 0.0
    angle = abs(raw_angle) % 360
    steps = abs(int(SPR * angle / 360))
    direction = CCW if raw_angle < 0 else CW
    return (steps, direction)

def biggest(a, y, z):
    Max = a
    if y > Max:
        Max = y
    if z > Max:
        Max = z
        if y > z:
            Max = y
    return Max

# rotate function
def rotate(steps, direction, pin_dir, pin_step, span_delay):
    print(span_delay)
    if not span_delay or not steps:
        return

    # GPIO.output(pin_dir, direction)
    pi.write(pin_dir, direction)
    for x in range(steps):
        pi.write(pin_step, 1)
        sleep(span_delay)
        pi.write(pin_step, 0)
        sleep(span_delay)

def drive_motors(deg1, deg2, deg3):
    (s_m1, d_m1) = arg_to_steps(deg1)
    (s_m2, d_m2) = arg_to_steps(deg2)
    (s_m3, d_m3) = arg_to_steps(deg3)

    max_step = biggest(s_m1, s_m2, s_m3)
    try:
        span_m1 = 0.5 * DELAY_PER_STEP * max_step / s_m1
    except:
        span_m1 = None

    try:
        span_m2 = 0.5 * DELAY_PER_STEP * max_step / s_m2
    except:
        span_m2 = None

    try:
        span_m3 = 0.5 * DELAY_PER_STEP * max_step / s_m3
    except:
        span_m3 = None

    # execute rotation using threading
    pin_direc = PIN_DIR_MOT1
    pin_step = PIN_STEP_MOT1
    t1 = threading.Thread(target=rotate, args=(s_m1, d_m1, pin_direc, pin_step, span_m1))
    pin_direc = PIN_DIR_MOT2
    pin_step = PIN_STEP_MOT2
    t2 = threading.Thread(target=rotate, args=(s_m2, d_m2, pin_direc, pin_step, span_m2))
    pin_direc = PIN_DIR_MOT3
    pin_step = PIN_STEP_MOT3
    t3 = threading.Thread(target=rotate, args=(s_m3, d_m3, pin_direc, pin_step, span_m3))

    # start execution
    t1.start()
    t2.start()
    t3.start()

    # wait until all motors finish rotation
    t1.join()
    t2.join()
    t3.join()

    #rotate(s_m1, d_m1, PIN_DIR_MOT1, PIN_STEP_MOT1, DELAY_PER_STEP)
    #rotate(s_m2, d_m2, PIN_DIR_MOT2, PIN_STEP_MOT2, DELAY_PER_STEP)
    #rotate(s_m3, d_m3, PIN_DIR_MOT3, PIN_STEP_MOT3, DELAY_PER_STEP)

