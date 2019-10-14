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

    # constants
    # w_disp = 640
    # h_disp = 480
    # THETA_START = 0.20101055250063418
    # THETA_CAMERA = 40.6204018472511
    # Z = 22.665998826723097
    # Y_START = -7.979529824079942
    # X_PERS = 3.6
    # W_TRUE_BOTTOM = 19.5

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
    rotate_servo(pwm, 40)
    sleep(0.5)
    pwm.stop()

def servo_open():
    pwm = GPIO.PWM(PIN_SERVO, 50)
    pwm.start(0.0)
    rotate_servo(pwm, 0)
    sleep(0.5)
    pwm.stop()

def move(x, y, z):
    # todo add param limit??
    z += z_home
    # y *= -1
    x *= -1
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive2.drive_motors((deg1, deg2, deg3))

def move_no_easing(x, y, z):
    # todo add param limit??
    z += z_home
    # y *= -1
    x *= -1
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive2.drive_motors_no_easing((deg1, deg2, deg3))

try:
    while True:
        if GPIO.input(PIN_BUTTON) == GPIO.LOW:

            is_outside = False
            try:
                x, y, w, h = dbconn.get_last_det()
            except:
                print 'db connection failed.'
            
            try:
                x_world, y_world = VWT(x, y, w, h)
                print 'target: [{}, {}]'.format(x_world, y_world)
            except:
                print 'error during transformation'

            if abs(x_world) > 100 or abs(y_world) > 100:
                is_outside = True 

            if not is_outside: 
                z_target = 15
                move(10 * x_world, 10 * y_world, z_target)
    
                servo_close()
                servo_open()
                servo_close()
                servo_open()
    
                # homing
                move(0, 0, 120)
    
                drive2.checkpoint()
            
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()

