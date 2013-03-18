import json
import cgi
import os
import sys
sys.path.append('/opt/Temperature-Sensor')
from database import Database
from sensor import Sensor, Sensor_Factory

def application(environ, start_response):
	status = '200 OK'
	input_data = cgi.parse_qs(environ['QUERY_STRING'])
	db = Database(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','temp.db'))
	sensors = Sensor_Factory(db).get_sensors()

	temp_data = {}
	for sens in sensors:
		if 'start' in input_data and 'end' in input_data:
			start = int(float(input_data['start'][0])/1000.0)
			end = int(float(input_data['end'][0])/1000.0)
		else:
			start = sens.get_date_of_first_entry()
			end = sens.get_date_of_last_entry()
			
		data = [(record[0]*1000,record[1]) for record in sens.get_data(start,end)]
		
		temp_data[sens.name] = data

	output = json.dumps(temp_data)

	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
	start_response(status, response_headers)

	return [output]
