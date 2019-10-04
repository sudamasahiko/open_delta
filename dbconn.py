import time, math
import mysql.connector

def get_last_det():
    now = (int)(time.time())
    sec_window = 6000
    conn = mysql.connector.connect(user='masahiko', password='ouse2007',
        host='169.254.9.245', database='plastic_ai')
    cur = conn.cursor()
    query = '''SELECT time, x, y, w, h FROM detection 
    ORDER BY time DESC limit 5;
    '''
    cur.execute(query)
    for row in cur.fetchall():
        x, y, w, h = row[1], row[2], row[3], row[4]
    cur.close
    conn.close
    return (x, y, w, h)

def ViewWorldTransforma(x_obj, y_obj, w_obj, h_obj):

    # constants
    W_VIEW = 640
    H_VIEW = 480
    Y_RAD_START = 0.2
    Y_RAD_CONST = 0.94
    Y_RAD_SIZE = -3.0
    X_RAD_SIZE = -2.0
    
    center_x_view = ((x_obj + 0.5 * w_obj) / W_VIEW - 0.5) * 2
    center_y_view = 1.0 - (y_obj + 0.5 * h_obj) / H_VIEW
    
    y_world = 7.8 - 10.7 * center_y_view\
        + Y_RAD_SIZE * math.tan(Y_RAD_START + Y_RAD_CONST * center_y_view)
    x_additional = X_RAD_SIZE * math.tan(Y_RAD_START + Y_RAD_CONST * center_y_view)
    x_world = -7.2 * center_x_view + x_additional * center_x_view
    return x_world, y_world

#x, y, w, h = get_last_det()
#x_world, y_world = ViewWorldTransforma(x, y, w, h)
#print(x_world)
#print(y_world)

