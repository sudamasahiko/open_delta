# coding: utf-8

# delta_robot.py
# usage: python delta_robot.py
# (C) Seltec Lab
# license: MIT LICENSE

import kinematics, dbconn, drive2
from time import sleep
import RPi.GPIO as GPIO

# pins
PIN_DIR_MOT1 = 27
PIN_STEP_MOT1 = 17
PIN_DIR_MOT2 = 10
PIN_STEP_MOT2 = 22
PIN_DIR_MOT3 = 13
PIN_STEP_MOT3 = 6
PIN_SERVO = 14
PIN_BUTTON = 4

# setting up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_SERVO, GPIO.OUT)
GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# mm from top
z_home = -352.323

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
    pass
    #pwm = GPIO.PWM(PIN_SERVO, 50)
    #pwm.start(0.0)
    #rotate_servo(pwm, 60)
    #sleep(0.5)
    #pwm.stop()

def servo_open():
    pass
    #pwm = GPIO.PWM(PIN_SERVO, 50)
    #pwm.start(0.0)
    #rotate_servo(pwm, 20)
    #sleep(0.5)
    #pwm.stop()

def move(x, y, z):
    z += z_home
    y *= -1
    x *= -1
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive2.drive_motors((deg1, deg2, deg3))

try:
    #pass
    x, y, w, h = dbconn.get_last_det()
    x_world, y_world = dbconn.ViewWorldTransforma(x, y, w, h)
    print 'target: [{}, {}]'.format(x_world, y_world)
except:
    print 'db connection failed.'
    pass

move(0, 0, 50)
sleep(1)

drive2.checkpoint()

GPIO.cleanup()

