import csv
import time
import datetime
import json

def application(environ, start_response):
	status = '200 OK'
	
	csvrdr  = csv.reader(open('/home/peter/Temperature-Sensor/temp.csv','rb'))

	s0 = []
	s1 = []
	s2 = []
	s3 = []

	for row in csvrdr:

		s = time.mktime(datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S').timetuple())
		s0.append([(long(s)*1000),float(row[1])])
		s1.append([(long(s)*1000),float(row[2])])
		s2.append([(long(s)*1000),float(row[3])])
		s3.append([(long(s)*1000),float(row[4])])
		data = {'Outside':s0,'Kitchen':s1,'Ceiling':s2,'Study':s3}
	output = json.dumps(data)

	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
