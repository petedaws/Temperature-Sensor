import sqlite3
import csv
import time
import datetime
import pprint


def query_raw_range(c,start,end):
	start_timestamp = time.mktime(start.timetuple())
	end_timestamp = time.mktime(end.timetuple())
	c.execute('SELECT * from raw_temperature_measurements where date between %d and %d' % (start_timestamp,end_timestamp))
	return c.fetchall()
	
def query_next(c):
	c.execute('SELECT * from ten_minute_temperature_measurements where date = (SELECT max(date) from ten_minute_temperature_measurements)')
	result = c.fetchall()
	if len(result) == 0:
		start = get_date_of_first_raw_entry(c)
	else:
		start = datetime.datetime.fromtimestamp(result[0][0])
	end = get_next_10_min_block(start)
	result = query_raw_range(c,start,end)
	if len(result) > 1:
		process_raw(c,result)
		return True
	elif len(result) == 1:
		return False
	else:
		return False

def process_raw(c,result):
	s0 = [i[1] for i in result]
	s1 = [i[2] for i in result]
	s2 = [i[3] for i in result]
	s3 = [i[4] for i in result]
	
	c.execute('INSERT INTO ten_minute_temperature_measurements VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
				result[-1][0],
				result[0][1],result[-1][1],min(s0),max(s0),
				result[0][2],result[-1][2],min(s1),max(s1),
				result[0][3],result[-1][3],min(s2),max(s2),
				result[0][4],result[-1][4],min(s3),max(s3),))

def get_date_of_first_raw_entry(c):
	c.execute('SELECT * from raw_temperature_measurements where date = (SELECT min(date) from raw_temperature_measurements)')
	timestamp_tuple = datetime.datetime.fromtimestamp(c.fetchall()[0][0])
	return get_next_10_min_block(timestamp_tuple)
	
def get_next_10_min_block(t):
	add_minutes = 10-(t.timetuple()[4]%10)
	if add_minutes == 0:
		add_mintues = 10
	d = datetime.timedelta(minutes=add_minutes)
	return t+datetime.timedelta(minutes=add_minutes)
	

def init():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	i = 0
	while (query_next(c)):
		print "commit " + str(i)
		i = i+1
	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	init()