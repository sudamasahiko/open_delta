# drive2.py
# License: MIT License

import time, sys, math, threading, copy
import RPi.GPIO as GPIO
import Adafruit_PCA9685

# constants for the motor
RESOLUTION = 4096
PULSE_WIDTH_MS = 20.0
PULSE_FROM = RESOLUTION * 0.5 / PULSE_WIDTH_MS
PULSE_TO = RESOLUTION * 2.5 / PULSE_WIDTH_MS
RANGE_ANGLE = 180
PORT_MOTOR1 = 15
PORT_MOTOR2 = 14
PORT_MOTOR3 = 13
RESOLUTION_MOTOR = 100
DELAY_STEP = 0.01
fn_calib = 'calibration.cfg'
fn_angles = 'angles_last.cfg'

# calibration for the motors
with open(fn_calib, 'r') as f:
    lines = f.readlines()
    f.close()

if len(lines) != 3:
    sys.exit()

calib = []
for line in lines:
    calib.append(float(line))

# saved angles
with open(fn_angles, 'r') as f:
    lines = f.readlines()
    f.close()

if len(lines) != 3:
    sys.exit()

angles_last = []
for line in lines:
    angles_last.append(float(line))

# init
# GPIO.setmode(GPIO.BOARD) # todo xxx should be removed?
pwm = Adafruit_PCA9685.PCA9685()
freq = int(1000 / PULSE_WIDTH_MS)
pwm.set_pwm_freq(freq)
ports = [PORT_MOTOR1, PORT_MOTOR2, PORT_MOTOR3]
angles_now = copy.copy(angles_last)

# functions
def get_pulse(angle):
    ratio_angle = angle / float(RANGE_ANGLE)
    pulse_target = int(PULSE_FROM + ratio_angle * (PULSE_TO - PULSE_FROM))
    return pulse_target

def set_angle(idx_motor, angle):
    for i in range(RESOLUTION_MOTOR):
        ratio = 1 - math.cos(math.pi * float(i+1) / RESOLUTION_MOTOR)
        ratio /= 2
        computed = calib[idx_motor] - angles_now[idx_motor] - ratio * (angle-angles_now[idx_motor])
        pwm.set_pwm(ports[idx_motor], 0, get_pulse(computed))
        time.sleep(DELAY_STEP)

def drive_motors(angles):
    global angles_now
    t1 = threading.Thread(target=set_angle, args=(0, angles[0]))
    t2 = threading.Thread(target=set_angle, args=(1, angles[1]))
    t3 = threading.Thread(target=set_angle, args=(2, angles[2]))
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    angles_now[0] = angles[0]
    angles_now[1] = angles[1]
    angles_now[2] = angles[2]
    time.sleep(1)

def checkpoint():
    global angles_now
    with open(fn_angles, 'w') as f:
        for ang in angles_now:
            f.write('{}\n'.format(ang))

# restore the saved angles
drive_motors(angles_last)

