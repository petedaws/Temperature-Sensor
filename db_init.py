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

def populate_index_tables(c,data):
	ten_minute_data = {}
	reset_index_data(ten_minute_data)
	for datum in data:
		check_10minute(c,datum,ten_minute_data)
			
def check_10minute(c,datum,ten_minute_data):
	threshold = 30
	timestamp_tuple = datetime.datetime.fromtimestamp(datum['timestamp'])
	if timestamp_tuple.timetuple()[5] <= threshold and timestamp_tuple.timetuple()[4] % 10 == 0:
		print 'start'
		print ten_minute_data
		#Found start of 10 minute period
		ten_minute_data['timestamp'] = datum['timestamp']
		ten_minute_data['start'] = {'s0':datum['s0'],'s1':datum['s1'],'s2':datum['s2'],'s3':datum['s3']}
		print ten_minute_data
		ten_minute_data['all']['s0'].append(datum['s0'])
		ten_minute_data['all']['s1'].append(datum['s1'])
		ten_minute_data['all']['s2'].append(datum['s2'])
		ten_minute_data['all']['s3'].append(datum['s3'])
	elif timestamp_tuple.timetuple()[5] >= threshold and timestamp_tuple.timetuple()[4] % 10 == 9:
		print 'end'
		#Found end of 10 minute period
		ten_minute_data['end'] = {'s0':datum['s0'],'s1':datum['s1'],'s2':datum['s2'],'s3':datum['s3']}
		ten_minute_data['low'] =  {'s0':min(ten_minute_data['all']['s0']),'s1':min(ten_minute_data['all']['s1']),'s2':min(ten_minute_data['all']['s2']),'s3':min(ten_minute_data['all']['s3'])}
		ten_minute_data['high'] = {'s0':max(ten_minute_data['all']['s0']),'s1':max(ten_minute_data['all']['s1']),'s2':max(ten_minute_data['all']['s2']),'s3':max(ten_minute_data['all']['s3'])}
		ten_minute_data['all']['s0'].append(datum['s0'])
		ten_minute_data['all']['s1'].append(datum['s1'])
		ten_minute_data['all']['s2'].append(datum['s2'])
		ten_minute_data['all']['s3'].append(datum['s3'])
		if not None in ten_minute_data.values():
			#All data exists, we can write to the DB
			pprint.pprint(ten_minute_data)
			c.execute('INSERT INTO ten_minute_temperature_measurements VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (
				ten_minute_data['timestamp'],
				ten_minute_data['start']['s0'],ten_minute_data['end']['s0'],ten_minute_data['low']['s0'],ten_minute_data['high']['s0'],
				ten_minute_data['start']['s1'],ten_minute_data['end']['s1'],ten_minute_data['low']['s1'],ten_minute_data['high']['s1'],
				ten_minute_data['start']['s2'],ten_minute_data['end']['s2'],ten_minute_data['low']['s2'],ten_minute_data['high']['s2'],
				ten_minute_data['start']['s3'],ten_minute_data['end']['s3'],ten_minute_data['low']['s3'],ten_minute_data['high']['s3']))
		#ten_minute_data['all'].clear()
		#ten_minute_data.clear()
		reset_index_data(ten_minute_data)
		print 'cleared'
		print ten_minute_data
	else:
		if ten_minute_data['start'] is not None:
			ten_minute_data['all']['s0'].append(datum['s0'])
			ten_minute_data['all']['s1'].append(datum['s1'])
			ten_minute_data['all']['s2'].append(datum['s2'])
			ten_minute_data['all']['s3'].append(datum['s3'])
		
def reset_index_data(data):
	data['timestamp'] = None
	data['start'] = None
	data['end'] = None
	data['low'] = None
	data['high'] = None
	all = {}
	all['s0'] = []
	all['s1'] = []
	all['s2'] = []
	all['s3'] = []
	data['all'] = all
	
	
	
def init_names(c):
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s0','Outside'))
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s1','Kitchen'))
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s2','Ceiling'))
	c.execute('INSERT INTO sensor_names VALUES ("%s","%s")' % ('s0','Study'))
			 
			 
def init():
	conn = sqlite3.connect('example.db')
	c = conn.cursor()
	create_tables(c)
	init_names(c)
	data = populate_raw_data(c)
	populate_index_tables(c,data)
	conn.commit()
	conn.close()
	
if __name__ == "__main__":
	init()