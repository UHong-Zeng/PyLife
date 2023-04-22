import sqlite3

conn = sqlite3.connect("Health.db")
cur = conn.cursor()
cur.execute("INSERT INTO HEALTH(ROW,COL,ISLIVE) values ({},{},{})".format(1,0,1))
conn.commit()
conn.close()