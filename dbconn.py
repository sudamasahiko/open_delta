import time
# import math
import mysql.connector

def get_last_det():
    now = (int)(time.time())
    sec_window = 6000
    conn = mysql.connector.connect(user='masahiko', password='ouse2007',
        host='169.254.9.245', database='plastic_ai')
    cur = conn.cursor()
    query = '''SELECT time, x, y, w, h
                 FROM detection 
                 ORDER BY time DESC;
    '''
    cur.execute(query)
    #for row in cur.fetchall():
    #    x, y, w, h = row[1], row[2], row[3], row[4]
    row = cur.fetchone()
    x, y, w, h = row[1], row[2], row[3], row[4]
    cur.close
    conn.close
    return (x, y, w, h)

# v1
# def ViewWorldTransforma(x_obj, y_obj, w_obj, h_obj):
# 
#     # constants
#     W_VIEW = 640
#     H_VIEW = 480
#     Y_RAD_START = 0.2
#     Y_RAD_CONST = 0.94
#     Y_RAD_SIZE = -3.0
#     X_RAD_SIZE = -2.0
#     
#     center_x_view = ((x_obj + 0.5 * w_obj) / W_VIEW - 0.5) * 2
#     center_y_view = 1.0 - (y_obj + 0.5 * h_obj) / H_VIEW
#     
#     y_world = 7.8 - 10.7 * center_y_view\
#         + Y_RAD_SIZE * math.tan(Y_RAD_START + Y_RAD_CONST * center_y_view)
#     x_additional = X_RAD_SIZE * math.tan(Y_RAD_START + Y_RAD_CONST * center_y_view)
#     x_world = -7.2 * center_x_view + x_additional * center_x_view
#     return x_world, y_world

# v2
# def ViewWorldTransforma(x_target, y_target, w_obj, h_obj):
# 
#     # constants
#     w_disp = 640
#     h_disp = 480
#     THETA_START = 0.20101055250063418
#     THETA_CAMERA = 40.6204018472511
#     Z = 22.665998826723097
#     Y_START = -7.979529824079942
#     X_PERS = 3.6
#     W_TRUE_BOTTOM = 19.5
#     Y_TOP = 11.6
#     Y_BUTTOM = -7.9
#     
#     y_norm = y_target / float(h_disp)
#     print 'y_target: {}'.format(y_target)
#     print 'y_norm: {}'.format(y_norm)
#     y_real = Y_START + Z * math.tan(math.radians(THETA_START + y_norm * THETA_CAMERA))
#     h_real = Y_TOP - Y_BUTTOM
#     w_additional = X_PERS * (y_real - Y_BUTTOM) / h_real
#     if x_target - 0.5 * w_disp < 0:
#         w_additional *= -1
#     x_real = (0.5 * W_TRUE_BOTTOM + w_additional) * (x_target - 0.5 * w_disp) / (0.5 * w_disp)
#     return x_real, y_real

