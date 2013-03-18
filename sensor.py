import time
import datetime
import re
from database import Database

SENSOR_INDEX_LEVELS = [30,10*60,30*60,60*60,6*60*60,12*60*60,24*60*60,7*60*60]

class Sensor_Factory:
	def __init__(self,db):
		self.db = db
	
	def get_sensors(self):
		tables = self.db.list_tables()
		sensors = []
		for table in tables:
			tab = re.match('(.*)(_raw)',table[0])
			if tab is not None:
				sensors.append(Sensor(tab.group(1),0,0,self.db))
		return sensors

class Sensor:
	
	def __init__(self,name,id,calibration_factor,db=None):
		self.name = name
		self.id = id
		self.__calibration_factor = calibration_factor
		self.db = db
		self.__init_database()

		
	def get_data(self, start, end, min_resolution=None):
		table = self.name+'_raw'
		return self.db.select('SELECT * from %s where date between %d and %d' % (table,start,end))
		
	def get_date_of_first_entry(self):
		table = self.name+'_raw'
		result = self.db.select('SELECT * from %s where date = (SELECT min(date) from %s)' % (table,table))
		if len(result) == 0:
			return None
		else:
			return int(result[0][0])
		
	def get_date_of_last_entry(self):
		table = self.name+'_raw'
		result = self.db.select('SELECT * from %s where date = (SELECT max(date) from %s)' % (table,table))
		if len(result) == 0:
			return None
		else:
			return int(result[0][0])
	
	def add_record(self,data):
		t = time.localtime()
		ts = time.mktime(t)
		self.db.add_record({
						'table_name':self.name+'_raw',
						'values':[int(ts),"%0.1f" % (data[self.id]+self.__calibration_factor)]})
		
	def __init_database(self):
		# create the raw data table
		self.db.create_table({
							'table_name':self.name + '_raw',
							'table_columns':[('date','integer'),('value','float')]})
