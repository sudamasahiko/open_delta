# coding: utf-8

# delta_robot.py
# usage: python delta_robot.py
# (C) Seltec Lab
# license: MIT LICENSE

import kinematics, drive
import RPi.GPIO as GPIO
import sys
from time import sleep
import dbconn

# pins
PIN_DIR_MOT1 = 27
PIN_STEP_MOT1 = 17
PIN_DIR_MOT2 = 10
PIN_STEP_MOT2 = 22
PIN_DIR_MOT3 = 13
PIN_STEP_MOT3 = 6
PIN_ENABLE = 19
PIN_SERVO = 14
PIN_BUTTON = 4

# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_DIR_MOT1, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT1, GPIO.OUT)
GPIO.setup(PIN_DIR_MOT2, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT2, GPIO.OUT)
GPIO.setup(PIN_DIR_MOT3, GPIO.OUT)
GPIO.setup(PIN_STEP_MOT3, GPIO.OUT)
GPIO.setup(PIN_ENABLE, GPIO.OUT)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# init GPIO pins
GPIO.output(PIN_DIR_MOT1, GPIO.LOW)
GPIO.output(PIN_STEP_MOT1, GPIO.LOW)
GPIO.output(PIN_DIR_MOT2, GPIO.LOW)
GPIO.output(PIN_STEP_MOT2, GPIO.LOW)
GPIO.output(PIN_DIR_MOT3, GPIO.LOW)
GPIO.output(PIN_STEP_MOT3, GPIO.LOW)
GPIO.output(PIN_ENABLE, GPIO.LOW)

# expected to be homed when startup
deg1_last, deg2_last, deg3_last = 0, 0, 0

# mm from top
#z_home = -181.5926
#z_home = -277.129
z_home = -280

def rotate_servo(servo, angle):
    #   0度の位置 0.5 ms / 20 ms * 100 = 2.5 %
    # 180度の位置 2.4 ms / 20 ms * 100 = 12 %
    #      変動幅 12% - 2.5% (9.5%)
    # angle * 9.5 / 180
    if -90 <= angle <= 90:
        d = ((angle + 90) * 9.5 / 180) + 2.5
        servo.ChangeDutyCycle(d)
    else:
        raise ValueError("angle")

def servo_close():
    pwm = GPIO.PWM(PIN_SERVO, 50)
    pwm.start(0.0)
    rotate_servo(pwm, 60)
    sleep(0.5)
    pwm.stop()

def servo_open():
    pwm = GPIO.PWM(PIN_SERVO, 50)
    pwm.start(0.0)
    rotate_servo(pwm, 20)
    sleep(0.5)
    pwm.stop()

def move(x, y, z):
    global deg1_last
    global deg2_last
    global deg3_last
    z += z_home
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive.drive_motors(deg1 - deg1_last, deg2 - deg2_last, deg3 - deg3_last)
        deg1_last = deg1
        deg2_last = deg2
        deg3_last = deg3
try:
    pass
    #x, y, w, h = dbconn.get_last_det()
    #x_world, y_world = dbconn.ViewWorldTransforma(x, y, w, h)
except:
    print('db connection failed.')
    pass

move(0, 0, 40)
sleep(1)
servo_open();
sleep(1)
servo_close();
move(0, 0, 10)

#move(0, 10, 30)
#sleep(0.5)
#move(10, 10, 30)
#sleep(0.5)
#move(10, -10, 30)
#sleep(0.5)
#move(-10, -10, 30)
#sleep(0.5)
#move(-10, 10, 30)
#sleep(0.5)
#move(0, 10, 30)
#sleep(0.5)
#move(0, 0, 0)
#sleep(2)

GPIO.cleanup()

