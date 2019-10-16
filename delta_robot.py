# delta_robot.py
# usage: python delta_robot.py
# (C) Seltec Lab
# license: MIT LICENSE

import kinematics, drive2
import RPi.GPIO as GPIO
import sys, json, math, time

# mm from top
z_home = -380.0

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

def move(x, y, z):
    z += z_home
    x *= -1
    x -= 1 # adjustment
    (err, deg1, deg2, deg3) = kinematics.inverse(x, y, z)
    if not err:
        drive2.drive_motors((deg1, deg2, deg3))

try:
    while True:
        x_in = float(input('x:'))
        y_in = float(input('y:'))
        z_in = float(input('z:'))
        print 'target: [{:.2f}, {:.2f}, {:.2f}]'.format(x_in, y_in, z_in)
        move(x_in, y_in, z_in)

except KeyboardInterrupt:
    print('\nterminating...')
    move(0, 0, 120)
    GPIO.cleanup()

