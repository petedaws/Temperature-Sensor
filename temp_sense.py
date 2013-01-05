#! /usr/bin/python
# RUN COMMAND:  nohup python "/home/pi/dev/temp_sense.py" start &

import serial
import time
import sys
import string
import platform
import csv
import datetime
import json

calibrations = {0:-4.4, 1:-1.2, 2: -2.2, 3: -3.0}

def output_json(datafile):
	csvrdr  = csv.reader(open(datafile,'rb'))

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
		data = {'s0':s0,'s1':s1,'s2':s2,'s3':s3}
	output_file = open('/var/www/temp_data.json','wb')
	output_file.write(json.dumps(data))
	output_file.close()

def average(data):
	readings = zip(*data)
	average_result = []
	for reading in readings:
		total = 0
		for sensor in reading:
			total += sensor
		average_result.append(total/float(len(reading)))
	return average_result
	
def calibrate(temp):
	for k,v in calibrations.iteritems():
		temp[k] += v
	return temp

def main(logname,ave_window):
	if platform.system() == 'Windows':
		serialport = serial.Serial("COM7", 9600)
	else:
		serialport = serial.Serial("/dev/ttyUSB0", 9600)
	temps = []
	while(True):
		tempstr = serialport.readline(None).strip()
		if not all(c in string.printable for c in tempstr):
			continue
		try:
			temp = [float(i) for i in tempstr.split(',')]
			temps.append(calibrate(temp))
		except:
			continue

		if len(temps) > ave_window:
			average_result = average(temps)
			log = open(logname,'a')
			tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
			log.write("".join((tm,',',",".join("%0.1f" % x for x in average_result),'\n')))
			log.close()
			temps = []
			output_json(logname)

if __name__ == "__main__":
	if sys.argv[1] == 'start':
		if platform.system() == 'Windows':
			main("temp.csv",300)
		else:
			main("/home/peter/Temperature-Sensor/temp.csv",300)
	else:
		sys.exit(0)


