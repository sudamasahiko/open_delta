# delta_robot.py
# usage: python delta_robot.py
# (C) Seltec Lab
# license: MIT LICENSE

import kinematics, drive
import RPi.GPIO as GPIO
import sys

# pins
PIN_DIR_MOT1 = 2
PIN_STEP_MOT1 = 3
PIN_DIR_MOT2 = 10
PIN_STEP_MOT2 = 22
PIN_DIR_MOT3 = 13
PIN_STEP_MOT3 = 6

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

try:
    while True:
        x_in = float(input('x:'))
        y_in = float(input('y:'))
        z_in = float(input('z:'))
        z_in += z_home

        # operations
        (err, deg1, deg2, deg3) = kinematics.inverse(x_in, y_in, z_in)
        if not err:
            drive.drive_motors(deg1 - deg1_last, deg2 - deg2_last, deg3 - deg3_last)
            #deg1_last = deg1 - deg1_last
            #deg2_last = deg2 - deg2_last
            #deg3_last = deg3 - deg3_last
            deg1_last = deg1
            deg2_last = deg2
            deg3_last = deg3
            print('{}, {}, {}'.format(deg1, deg2, deg3))
            print('{}, {}, {}'.format(deg1_last, deg2_last, deg3_last))

except KeyboardInterrupt:
    print('\nterminating...')
    GPIO.cleanup()
    sys.exit()

