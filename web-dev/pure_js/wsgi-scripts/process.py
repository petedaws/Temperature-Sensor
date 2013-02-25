import time
import datetime
import json
import sqlite3

def application(environ, start_response):
	status = '200 OK'
	conn = sqlite3.connect('/home/peter/Temperature-Sensor/temp.db')
	c = conn.cursor()
	
	table = 'raw_temperature_measurements'
	c.execute('SELECT * from %s' % (table))
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
