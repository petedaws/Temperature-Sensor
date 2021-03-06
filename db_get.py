#TODO:
# 1) Make the code agnostic to the number of sensors

import sqlite3
import csv
import time
import datetime
import pprint


def query_range(c,table,start,end):
	start_timestamp = time.mktime(start.timetuple())
	end_timestamp = time.mktime(end.timetuple())
	c.execute('SELECT * from %s where date between %d and %d' % (table,start_timestamp,end_timestamp))
	return c.fetchall()
	
def populate_index_table_block(c,process_table,source_table,start,time_block,min_result_size):
	if start is None:
		start = get_date_of_last_entry(c,process_table)
	if start is None:
		#no entries currently exist in the index table
		start = get_date_of_first_entry(c,source_table)
		if start is None:
			return False,None
	end = start+time_block
	if end+time_block < get_date_of_last_entry(c,source_table):
		result = query_range(c,source_table,start,end)
		if len(result) >= min_result_size:
			# did we query the raw table or and index table?
			if len(result[0]) > 5:
				process_index(c,process_table,result)
			else:
				process_raw(c,result)
			print '%s on: %s, length: %s' % (process_table,end,len(result)) ##Debug
		else:
			print 'missing data for %s on %s, length: %s' % (process_table,end,len(result)) ##Debug
		return True,end
	else:
		print 'end of %s data at %s' % (process_table,end)##Debug
		return False,None
		
def process_index(c,table,result):
	s0_low = [i[3] for i in result]
	s0_high = [i[4] for i in result]
	s1_low = [i[7] for i in result]
	s1_high = [i[8] for i in result]
	s2_low = [i[7] for i in result]
	s2_high = [i[8] for i in result]
	s3_low = [i[11] for i in result]
	s3_high = [i[12] for i in result]
	s4_low = [i[15] for i in result]
	s4_high = [i[16] for i in result]
	
	
	c.execute('INSERT INTO %s VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
			table,
			result[-1][0],
			result[0][1],result[-1][2],min(s0_low),max(s0_high),
			result[0][5],result[-1][6],min(s1_low),max(s1_high),
			result[0][9],result[-1][10],min(s2_low),max(s2_high),
			result[0][13],result[-1][14],min(s3_low),max(s3_high),))
			
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


def get_date_of_first_entry(c,table):
	c.execute('SELECT * from %s where date = (SELECT min(date) from %s)' % (table,table))
	result = c.fetchall()
	if len(result) == 0:
		return None
	else:
		timestamp_tuple = datetime.datetime.fromtimestamp(result[0][0])
	return timestamp_tuple
	
def get_date_of_last_entry(c,table):
	c.execute('SELECT * from %s where date = (SELECT max(date) from %s)' % (table,table))
	result = c.fetchall()
	if len(result) == 0:
		return None
	else:
		timestamp_tuple = datetime.datetime.fromtimestamp(result[0][0])
		return timestamp_tuple

def process_index_table(conn,process_table,source_table,time_block,min_result_size):
	c = conn.cursor()
	start = None
	index_incomplete = True 
	while index_incomplete:
		index_incomplete,start = populate_index_table_block(c,
													process_table,
													source_table,
													start,
													time_block,
													min_result_size)
	conn.commit()
	
def init():
	conn = sqlite3.connect('temp.db')
	process_index_table(conn,'ten_minute_temperature_measurements','raw_temperature_measurements',datetime.timedelta(minutes=10),10)
	process_index_table(conn,'half_hour_temperature_measurements','ten_minute_temperature_measurements',datetime.timedelta(minutes=30),1)
	process_index_table(conn,'hour_temperature_measurements','ten_minute_temperature_measurements',datetime.timedelta(hours=1),1)
	process_index_table(conn,'six_hour_temperature_measurements','hour_temperature_measurements',datetime.timedelta(hours=6),1)
	process_index_table(conn,'twelve_hour_temperature_measurements','hour_temperature_measurements',datetime.timedelta(hours=12),1)
	process_index_table(conn,'daily_temperature_measurements','hour_temperature_measurements',datetime.timedelta(days=1),1)
	process_index_table(conn,'weekly_temperature_measurements','daily_temperature_measurements',datetime.timedelta(days=7),1)
	process_index_table(conn,'monthly_temperature_measurements','daily_temperature_measurements',datetime.timedelta(days=30),1)
	conn.close()
	
if __name__ == "__main__":
	init()