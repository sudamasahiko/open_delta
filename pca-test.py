# pca-test.py
# manually drive 3 servo motors
# usage: python pca-test.py [options] [angle1] [angle2] [angle3]
# options: -e, --easing: enable easing
# (C) Seltec Lab
# License: MIT License

import time, sys, math, threading, copy, argparse
import Adafruit_PCA9685

# constants for PCA9685 the motor driver
RESOLUTION = 4096
PORT_MOTOR1 = 15
PORT_MOTOR2 = 14
PORT_MOTOR3 = 13

# specs of the servo LD-25MG in this case
PULSE_WIDTH_MS = 20.0
PULSE_FROM = RESOLUTION * 0.5 / PULSE_WIDTH_MS
PULSE_TO = RESOLUTION * 2.5 / PULSE_WIDTH_MS
RANGE_ANGLE = 180

# params for easing and speed
RESOLUTION_MOTOR = 100
DELAY_STEP = 0.005

# config files
fn_calib = 'calibration.cfg'
fn_angles = 'angles_last.cfg'

# params
parser = argparse.ArgumentParser()
parser.add_argument('angle1', type=float)
parser.add_argument('angle2', type=float)
parser.add_argument('angle3', type=float)
parser.add_argument('-e', '--easing', action='store_true')
IS_EASEING = True if args.easing else IS_EASEING = False

# calibration for the motors
calib = []
with open(fn_calib, 'r') as f:
    lines = f.readlines()
    f.close()

if len(lines) != 3:
    sys.exit(1)

for line in lines:
    calib.append(float(line))

# saved angles
with open(fn_angles, 'r') as f:
    lines = f.readlines()
    f.close()

if len(lines) != 3:
    sys.exit(1)

angles_last = []
for line in lines:
    angles_last.append(float(line))

# entry point
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
    if IS_EASEING:
        for i in range(RESOLUTION_MOTOR):
            ratio = 1 - math.cos(math.pi * float(i+1) / RESOLUTION_MOTOR)
            ratio /= 2
            computed = calib[idx_motor] - angles_now[idx_motor] - ratio * (angle-angles_now[idx_motor])
            pwm.set_pwm(ports[idx_motor], 0, get_pulse(computed))
            time.sleep(DELAY_STEP)
    else:
        pwm.set_pwm(ports[idx_motor], 0, get_pulse(angle))

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

# new angles
drive_motors((args.angle1, args.angle2, args.angle3))

# save present angles to the config file
with open(fn_angles, 'w') as f:
    for ang in angles_now:
        f.write('{}\n'.format(ang))

