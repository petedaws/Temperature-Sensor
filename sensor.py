import sqlite3
import csv
import time
import datetime

SENSOR_INDEX_LEVELS = [30,10*60,30*60,60*60,6*60*60,12*60*60,24*60*60,7*60*60]

class sensor:
	
	def __init__(self,name,id):
		self.name = name
		self.id = id
	
	def get_range(self, start, end):
		start_timestamp = time.mktime(start.timetuple())
		end_timestamp = time.mktime(end.timetuple())
		c.execute('SELECT * from %s where date between %d and %d' % (table,start_timestamp,end_timestamp))
		return c.fetchall()
	
	def add_data(self,data):
		None #TODO
		
	