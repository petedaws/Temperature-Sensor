#! /usr/bin/python
import platform
import serial
import string

class Serial_Reactor:

	def __init__(self,serial_port,ave_window):
		self.__ave_window = ave_window
		self.__events = {}
		self.__trace = True
		if platform.system() == 'Windows':
			self.__serialport = serial.Serial(serial_port, 9600)
		else:
			self.__serialport = serial.Serial(serial_port, 9600)
	
	def connect_event(self, event_name, callback):
		assert callable(callback)
		if self.__trace:
			print 'connect_event', event_name, callback
		if event_name in self.__events:
			self.__events[event_name].append(callback)
		else:
			self.__events[event_name] = [callback]
	
	def __average(self,data):
		readings = zip(*data)
		average_result = []
		for reading in readings:
			total = 0
			for sensor in reading:
				total += sensor
			average_result.append(total/float(len(reading)))
		return average_result
	
	def run(self):
		temps = []
		while(True):
			tempstr = self.__serialport.readline(None).strip()
			if not all(c in string.printable for c in tempstr):
				continue
			try:
				temp = [float(i) for i in tempstr.split(',')]
				temps.append(temp)
			except:
				continue
				
			if len(temps) > self.__ave_window:
				self.trigger_event('sensor_reading',self.__average(temps))
				temps = []


	def trigger_event(self, event_name, *args):
		if self.__trace:
			print 'trigger_event', event_name, args
		if event_name in self.__events:
			for cb in self.__events[event_name]:
				cb(*args)
	
if platform.system() == 'Windows':
	serial_reactor = Serial_Reactor('COM7',300)
else:
	serial_reactor = Serial_Reactor('/dev/ttyUSB0',300)



