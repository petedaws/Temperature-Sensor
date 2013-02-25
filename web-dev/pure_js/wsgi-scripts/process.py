import time
import datetime
import json
import sqlite3

def application(environ, start_response):
	status = '200 OK'
	conn = sqlite3.connect('temp.db')
	c = conn.cursor()
	
	table = 'raw_temperature_measurements'
	data = c.execute('SELECT * from %s' % (table))

	s0 = []
	s1 = []
	s2 = []
	s3 = []

	for row in data:

		s = row[0]
		s0.append([(long(s)*1000),float(row[1])])
		s1.append([(long(s)*1000),float(row[2])])
		s2.append([(long(s)*1000),float(row[3])])
		s3.append([(long(s)*1000),float(row[4])])
		data = {'Outside':s0,'Kitchen':s1,'Ceiling':s2,'Study':s3}
	output = json.dumps(data)

	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
