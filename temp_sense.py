#! /usr/bin/python
# RUN COMMAND:  nohup python "/home/pi/dev/temp_sense.py" start &

import serial
import time
import sys
import string

def main(logname):
	serialport = serial.Serial("/dev/ttyUSB0", 9600)
	while(True):
		temps = serialport.readline(None).strip()
		if not all(c in string.printable for c in temps):
			continue
		log = open(logname,'a')
		tm = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
		log.write("".join((tm,',',temps,'\n')))
		log.close()

if __name__ == "__main__":
	if sys.argv[1] == 'start':
		main("/home/pi/temp.csv")
	else:
		sys.exit(0)


