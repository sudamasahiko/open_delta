import time
import mysql.connector

USR = 'masahiko'
PWD = 'ouse2007'
HOST = '169.254.9.245'
DB = 'plastic_ai'

def get_last_det():
    now = (int)(time.time())
    sec_window = 6000
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
    x, y, w, h = row[1], row[2], row[3], row[4]
    cur.close
    conn.close
    return (x, y, w, h)

# delete everything
def flush():
    conn = mysql.connector.connect(user=USR, password=PWD, host=HOST, database=DB)
    cur = conn.cursor()
    query = 'DELETE FROM detection;'
    cur.execute(query)
    cur.close
    conn.close

def in_db(t_since, x, y, w, h):
    conn = mysql.connector.connect(user=USR, password=PWD, host=HOST, database=DB)
    cur = conn.cursor()
    query = '''SELECT COUNT(1) FROM detection
      WHERE time > {} AND x > x-30 AND x < x+30
        AND y > y-30 AND y < y+30
        AND w > w-30 AND w < w+30
        AND h > h-30 AND h < h+30
      ;'''.format(t_since)
        cur.execute(query)
        row = cur.fetchone()
        cnt = row[1]
        cur.close
        conn.close
        if cnt > 0:
            return True
        else:
            return False
