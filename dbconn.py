import time
import mysql.connector

USR = 'masahiko'
PWD = 'ouse2007'
HOST = '169.254.9.245'
DB = 'plastic_ai'

def get_last_det():
    now = (int)(time.time())
    sec_window = 10
    conn = mysql.connector.connect(user=USR, password=PWD, host=HOST, database=DB)
    cur = conn.cursor()
    query = '''SELECT time, x, y, w, h
                 FROM detection
                 ORDER BY time DESC;
    '''
    cur.execute(query)
    #for row in cur.fetchall():
    #    x, y, w, h = row[1], row[2], row[3], row[4]
    row = cur.fetchone()
    cur.close
    conn.close
    try:
        x, y, w, h = row[1], row[2], row[3], row[4]
    except:
        x, y, w, h = None, None, None, None
    return (x, y, w, h)

# delete everything
def flush():
    conn = mysql.connector.connect(user=USR, password=PWD, host=HOST, database=DB)
    cur = conn.cursor()
    query = 'DELETE FROM detection;'
    cur.execute(query)
    conn.commit()
    cur.close
    conn.close

def in_db(x, y, w, h):
    conn = mysql.connector.connect(user=USR, password=PWD, host=HOST, database=DB)
    cur = conn.cursor()
    query = '''SELECT x,y,w,h FROM detection
      WHERE x > {} AND x < {}
        AND y > {} AND y < {}
      ;'''.format(x-90, x+90, y-90, y+90)
    print(query)

    # query = '''SELECT time,x,y,w,h FROM detection;'''

    cur.execute(query)
    rows = cur.fetchall()
    # cnt = row[0]
    cnt = len(rows)
    print('cnt: {}'.format(len(rows)))
    cur.close
    conn.close
    if cnt > 0:
        return True
    else:
        return False

