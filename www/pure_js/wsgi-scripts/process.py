import time
import datetime
import json
import sqlite3
import pprint
import cgi

def get_resolve_query(start,end):
	start_ts = datetime.datetime.fromtimestamp(start)
	end_ts = datetime.datetime.fromtimestamp(end)
	
	range = end_ts-start_ts
	
	resolve = [(datetime.timedelta(hours=1),'ten_minute_temperature_measurements'),
			   (datetime.timedelta(days=20),'half_hour_temperature_measurements'),
			   (datetime.timedelta(days=100),'hour_temperature_measurements'),
			   (datetime.timedelta(days=365),'daily_temperature_measurements')]
	
	query = 'SELECT * from %s where date between %d and %d' % ('daily_temperature_measurements',start,end)
	for reduction in resolve:
		if range < reduction[0]:
			query = 'SELECT * from %s where date between %d and %d' % (reduction[1],start,end)
			return query
	return query
	
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

def application(environ, start_response):
	status = '200 OK'
	input_data = cgi.parse_qs(environ['QUERY_STRING'])
	conn = sqlite3.connect('C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs\\wsgi-scripts\\temp.db')
	c = conn.cursor()
	
	if 'start' in input_data and 'end' in input_data:
		start = int(input_data['start'][0])
		end = int(input_data['end'][0])
	else:
		start = time.mktime(get_date_of_first_entry(c,'raw_temperature_measurements').timetuple())
		end = time.mktime(get_date_of_last_entry(c,'raw_temperature_measurements').timetuple())

	query = get_resolve_query(start,end)
	c.execute(query)
	data = c.fetchall()
	conn.close()
	pivot = zip(*data)
	s0 = zip(pivot[0],pivot[1])
	s1 = zip(pivot[0],pivot[5])
	s2 = zip(pivot[0],pivot[9])
	s3 = zip(pivot[0],pivot[13])

	data = {'Outside':s0,'Kitchen':s1,'Ceiling':s2,'Study':s3}
	output = json.dumps(data)

	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
