# delta_robot.py
# usage: python delta_robot.py
# (C) Seltec Lab
# license: MIT LICENSE

import kinematics, drive
import RPi.GPIO as GPIO
import sys
from time import sleep

# pins
PIN_DIR_MOT1 = 20
PIN_STEP_MOT1 = 21
PIN_DIR_MOT2 = 5
PIN_STEP_MOT2 = 6
PIN_DIR_MOT3 = 13
PIN_STEP_MOT3 = 19

# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR_MOT1, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT1, GPIO.OUT)
GPIO.setup(PIN_DIR_MOT2, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT2, GPIO.OUT)
GPIO.setup(PIN_DIR_MOT3, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT3, GPIO.OUT)

# init GPIO pins
GPIO.output(PIN_DIR_MOT1, GPIO.LOW)
GPIO.output(PIN_STEP_MOT1, GPIO.LOW)
GPIO.output(PIN_DIR_MOT2, GPIO.LOW)
GPIO.output(PIN_STEP_MOT2, GPIO.LOW)
GPIO.output(PIN_DIR_MOT3, GPIO.LOW)
GPIO.output(PIN_STEP_MOT3, GPIO.LOW)

# expected to be homed when startup
deg1_last, deg2_last, deg3_last = 0, 0, 0

# mm from top
z_home = -181.5926

def move(x, y, z):
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive.drive_motors(deg1 - deg1_last, deg2 - deg2_last, deg3 - deg3_last)
        deg1_last = deg1
        deg2_last = deg2
        deg3_last = deg3

n_repeat = 3

for x in range(n_repeat):
    move(0, 0, -50)
    sleep(0.5)
    move(40, 40, -50)
    sleep(0.5)
    move(40, -40, -50)
    sleep(0.5)
    move(-40, -40, -50)
    sleep(0.5)
    move(-40, 40, -50)
    sleep(0.5)
    move(0, 0, 0)
    sleep(2)

GPIO.cleanup()

