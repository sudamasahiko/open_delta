# coding: utf-8

# delta_robot.py
# usage: python delta_robot.py
# (C) Seltec Lab
# license: MIT LICENSE

import kinematics, dbconn, drive2
from time import sleep
import math, json
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

# load saved parameters
fn = 'camera_params.json'
with open(fn, 'r') as f:
    raw = f.read()
    f.close()
params = json.loads(raw)
for param in params:
    params[param] = float(params[param])

# View-world Transformation
def VWT(x_target, y_target, w_obj, h_obj):
    global params
    Y_TOP = params['y1_true']
    Y_BOTTOM = params['y3_true']
    y_norm = y_target / float(params['h_disp'])
    y_real = params['y_start'] + params['z'] * math.tan(math.radians(params['theta_start'] + y_norm * params['theta_camera']))
    h_real = Y_TOP - Y_BOTTOM
    w_additional = params['x_pers'] * (y_real - Y_BOTTOM) / h_real
    if x_target - 0.5 * params['w_disp'] < 0:
        w_additional *= -1
    x_real = (0.5 * params['w_true_bottom'] + w_additional) * (x_target - 0.5 * params['w_disp']) / (0.5 * params['w_disp'])
    return x_real, y_real

def rotate_servo(servo, angle):
    if -90 <= angle <= 90:
        d = ((angle + 90) * 9.5 / 180) + 2.5
        servo.ChangeDutyCycle(d)
    else:
        raise ValueError("angle")

def servo_close(angle=30, wait=0.5):
    pwm = GPIO.PWM(PIN_SERVO, 50)
    pwm.start(0.0)
    rotate_servo(pwm, angle)
    sleep(wait)
    pwm.stop()

def servo_open(wait=0.5):
    pwm = GPIO.PWM(PIN_SERVO, 50)
    pwm.start(0.0)
    rotate_servo(pwm, 0)
    sleep(wait)
    pwm.stop()

def move(x, y, z):
    z += z_home
    x *= -1
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive2.drive_motors((deg1, deg2, deg3))

def move_no_easing(x, y, z):
    z += z_home
    x *= -1
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive2.drive_motors_no_easing((deg1, deg2, deg3))

def maneuver():
    is_outside = False
    try:
        x, y, w, h = dbconn.get_last_det()
    except:
        print 'db connection failed.'
        import traceback
        traceback.print_exc()

    try:
        x_world, y_world = VWT(x, y, w, h)
        print 'target: [{:.2f}, {:.2f}]'.format(x_world, y_world)
    except:
        import traceback
        traceback.print_exc()

    limit = 100.0
    if abs(x_world) > limit or abs(y_world) > limit:
        is_outside = True

    if not is_outside:
        z_target = 15


        is_target_stays = True
        cnt = 0
        cnt_try = 5
        grip_anble_base = 40
        while is_target_stays and cnt < cnt_try:
            cnt += 1
            move(10 * x_world, 10 * y_world, z_target)

            # grip size will become stronger
            servo_close(grip_anble_base)
            servo_open()
            servo_close(grip_anble_base)
            servo_open()
            grip_angle = grip_anble_base + cnt * 2
            servo_close(grip_angle)

            # lift and check
            move(0, 0, 120)
            t_window = 2
            sleep(t_window)
            dbconn.flush()
            t_since = int(time.time()) - t_window
            if not dbconn.in_db(t_since, x, y, w, h):
                is_target_stays = False
                move(0, 80, 120)
                servo_open()
                move(0, 0, 120)
            else:
                servo_open()

        drive2.checkpoint()

try:
    while True:
        if GPIO.input(PIN_BUTTON) == GPIO.LOW:
            maneuver()

except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

