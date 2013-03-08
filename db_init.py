import sqlite3
import csv
import time
import datetime
import pprint

def create_tables(c):
	c.execute('''CREATE TABLE raw_temperature_measurements
			 (date integer, s0 real, s1 real, s2 real, s3 real)''')
			 
	c.execute('''CREATE TABLE ten_minute_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')
			 
	c.execute('''CREATE TABLE half_hour_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')
			 
	c.execute('''CREATE TABLE hour_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')
			 
	c.execute('''CREATE TABLE six_hour_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')
			 
	c.execute('''CREATE TABLE twelve_hour_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')
			 
	c.execute('''CREATE TABLE daily_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')
			 
	c.execute('''CREATE TABLE weekly_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')

	c.execute('''CREATE TABLE monthly_temperature_measurements
			 (date integer, s0_start real, s0_end real, s0_low real, s0_high real, s1_start real, s1_end real, s1_low real, s1_high real, s2_start real, s2_end real, s2_low real, s2_high real,s3_start real, s3_end real, s3_low real, s3_high real)''')

 	c.execute('''CREATE TABLE sensor_names
			 (sensor_id text, name text)''')
 
def populate_raw_data(c):
	csvrdr  = csv.reader(open('temp.csv','rb'))

	s0 = []
	s1 = []
	s2 = []
	s3 = []
	output = []
	for row in csvrdr:
		s = time.mktime(datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S').timetuple())
		s0.append([(long(s)*1000),float(row[1])])
		s1.append([(long(s)*1000),float(row[2])])
		s2.append([(long(s)*1000),float(row[3])])
		s3.append([(long(s)*1000),float(row[4])])
		output.append({'timestamp':int(s),'s0':float(row[1]),'s1':float(row[2]),'s2':float(row[3]),'s3':float(row[4])})
		c.execute("INSERT INTO raw_temperature_measurements VALUES (%d,%f,%f,%f,%f)" % (int(s),float(row[1]),float(row[2]),float(row[3]),float(row[4])))
	return output
	
	
	
def init_names(c):
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s0','Outside'))
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s1','Kitchen'))
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s2','Ceiling'))
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s3','Study'))
			 
			 
def init():
	conn = sqlite3.connect('temp.db')
	c = conn.cursor()
	create_tables(c)
	init_names(c)
	data = populate_raw_data(c)
	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	init()