import sqlite3
import csv
import time
import datetime
import pprint


def get_raw_range(c,start,end):
	start_timestamp = time.mktime(datetime.datetime.strptime(start,'%Y-%m-%d %H:%M:%S').timetuple())
	end_timestamp = time.mktime(datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S').timetuple())
	c.execute('SELECT * from raw_temperature_measurements where date between %d and %d' % (start_timestamp,end_timestamp))
	pprint.pprint(c.fetchall())
	
	
def init():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	get_raw_range(c,'2013-01-06 23:00:00','2013-01-06 23:05:00')
	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	init()