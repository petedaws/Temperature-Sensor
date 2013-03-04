import time
import datetime
from database import database

SENSOR_INDEX_LEVELS = [30,10*60,30*60,60*60,6*60*60,12*60*60,24*60*60,7*60*60]

class sensor:
	
	def __init__(self,name,id,calibration_factor):
		self.name = name
		self.id = id
		self.__calibration_factor = calibration_factor
		self.__init_database()
		serial_reactor.connect_event('sensor_reading',self.add_record)
		

	def get_data(self, start, end, min_resolution):
		start_timestamp = time.mktime(start.timetuple())
		end_timestamp = time.mktime(end.timetuple())
		c.execute('SELECT * from %s where date between %d and %d' % (table,start_timestamp,end_timestamp))
		return c.fetchall()
	
	def add_record(self,data):
		t = time.localtime()
		ts = time.mktime(t)
		database.add_record({
						'table_name':self.name+'_raw',
						'values':[int(ts),data[id]+self.__calibration_factor]})
		
	def __init_database(self):
		# create the raw data table
		database.create_table({
							'table_name':self.name + '_raw',
							'table_columns':[('date','integer'),('value','float')]})