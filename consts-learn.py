# coding: utf-8

import math, random, json

# load saved parameters
fn = 'camera_params.json'
with open(fn, 'r') as f:
    raw = f.read()
    f.close()
params = json.loads(raw)
for param in params:
    params[param] = float(params[param])

print 'loaded params:'
for k,v in params.items():
    print '{}: {}'.format(k, v)

def calc_loss(theta_start_in, theta_camera_in, z_in, y_start_in, fac):
    rand0 = fac * (random.random() - 0.5)
    rand1 = fac * (random.random() - 0.5)
    rand2 = fac * (random.random() - 0.5)
    rand3 = fac * (random.random() - 0.5)
    theta_start = theta_start_in + rand0
    theta_camera = theta_camera_in + rand1
    z = z_in + rand2
    y_start = y_start_in + rand3

    y1 = y_start + z * math.tan(math.radians(theta_start + theta_camera))
    y2 = y_start + z * math.tan(math.radians(theta_start + 0.5 * theta_camera))
    y3 = y_start + z * math.tan(math.radians(theta_start))
    y1_true = 11.6
    y2_true = 0.5
    y3_true = -7.9
    loss = math.pow(y1 - y1_true, 2) + math.pow(y2 - y2_true, 2) + math.pow(y3 - y3_true, 2)
    return loss, theta_start, theta_camera, z, y_start

class Param():
    def __init__(self, loss, theta_start, theta_camera, z, y_start):
        self.loss = loss
        self.theta_start = theta_start
        self.theta_camera = theta_camera
        self.z = z
        self.y_start = y_start

    def __lt__(self, other):
        # self < other
        return self.loss < other.loss

# starter params
theta_start = params['theta_start']
theta_camera = params['theta_camera']
z = params['z']
y_start = params['y_start']

# start learning
n_gen = 500
n_epoch = 2000
for i in range(n_epoch):

    children = []
    for j in range(n_gen):
        factor = 0.01 if j > 0 else 0

        loss_ret, theta_start_ret, theta_camera_ret, z_ret, y_start_ret = calc_loss(theta_start, theta_camera, z, y_start, factor)
        child = Param(loss_ret, theta_start_ret, theta_camera_ret, z_ret, y_start_ret)
        children.append(child)

    # 0th is the best
    children = sorted(children)
    theta_start, theta_camera, z, y_start = children[0].theta_start, children[0].theta_camera, children[0].z, children[0].y_start
    if i == 0:
        print ''
    if i % 500 == 0:
        print 'epoch: {}, loss: {}'.format(i, children[0].loss)

# results
best = children[0]
params['theta_start'] = best.theta_start
params['theta_camera'] = best.theta_camera
params['z'] = best.z
params['y_start'] = best.y_start
data = json.dumps(params, indent=4)
fn = 'camera_params.json'
with open(fn, 'w') as f:
    f.write(data)
    f.close()

# test
# x_target = 333
# y_target = 224
#
# y_norm = y_target / params['h_disp']
# y_real = params['y_start'] + params['z'] * math.tan(math.radians(params['theta_start'] + y_norm * params['theta_camera']))
# x_additional = params['x_pers'] * (y_real - params['y3_true']) / (params['y1_true'] - params['y3_true'])
# x_real = params['w_true_bottom'] * (x_target - 0.5 * params['w_disp']) / (0.5 * params['w_disp']) + x_additional

print '\nlearned params:'
for k,v in params.items():
    print '{}: {}'.format(k, v)

