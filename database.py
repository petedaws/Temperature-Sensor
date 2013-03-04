import sqlite3
import csv
import time
import datetime

class Database:
	
	def __init__(self,db_path):
		self.conn = sqlite3.connect(db_path)
		
	def table_exists(self,table_details):
		c = self.conn.cursor()
		c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="%s"' % (table_details['table_name'])) 
		if len(c.fetchall()) > 0:
			return True
		else:
			return False

	def create_table(self,table_details):
		c = self.conn.cursor()
		if not table_exists(table_details):
			columns = ','.join([' '.join([i[0],i[1]]) for i in table_details['columns']])
			c.execute('CREATE TABLE %s (%s)' % (table_details['table_name'],columns))
			self.conn.commit()

	def add_record(self,record):
		values = ','.join(record['values'])
		c.execute("INSERT INTO %s VALUES (%s)" % (record['table_name'],values))
		conn.commit()

database = Database('test.db')
		
if __name__ == '__main__':
	assert not database.table_exists({'table_name':'rww'})
	assert database.table_exists({'table_name':'raw_temperature_measurements'})