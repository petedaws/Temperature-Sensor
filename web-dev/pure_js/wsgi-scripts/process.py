import time
import datetime
import json
import sqlite3
import pprint
import cgi

def application(environ, start_response):
	status = '200 OK'
	input_data = cgi.parse_qs(environ['QUERY_STRING'])
	conn = sqlite3.connect('C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs\\wsgi-scripts\\temp.db')
	c = conn.cursor()
	
	if 'start' in input_data and 'end' in input_data:
		table = 'ten_minute_temperature_measurements'
		query = 'SELECT * from %s where date between %d and %d' % (table,int(input_data['start'][0]),int(input_data['end'][0]))
	else:
		table = 'hour_temperature_measurements'
		query = 'SELECT * from %s' % (table)
	c.execute(query)
	data = c.fetchall()
	conn.close()
	pivot = zip(*data)
	s0 = zip(pivot[0],pivot[1])
	s1 = zip(pivot[0],pivot[2])
	s2 = zip(pivot[0],pivot[3])
	s3 = zip(pivot[0],pivot[4])

	data = {'Outside':s0,'Kitchen':s1,'Ceiling':s2,'Study':s3}
	output = json.dumps(data)

	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
