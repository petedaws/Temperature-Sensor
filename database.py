import sqlite3
import csv
import time
import datetime

class Database:
	
	def __init__(self,db_path):
		self.conn = sqlite3.connect(db_path)
		
	def table_exists(self,table_name):
		c = self.conn.cursor()
		c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="%s"' % (table_name)) 
		if len(c.fetchall()) > 0:
			return True
		else:
			return False
			
	def list_tables(self):
		c = self.conn.cursor()
		c.execute('SELECT name FROM sqlite_master WHERE type="table"')
		return c.fetchall()

	def create_table(self,table_details):
		c = self.conn.cursor()
		if not self.table_exists(table_details['table_name']):
			columns = ','.join([' '.join([i[0],i[1]]) for i in table_details['table_columns']])
			c.execute('CREATE TABLE %s (%s)' % (table_details['table_name'],columns))
			self.conn.commit()

	def add_record(self,record,commit=True):
		c = self.conn.cursor()
		values = ','.join([str(val) for val in record['values']])
		query = "INSERT INTO %s VALUES (%s)" % (record['table_name'],values)
		c.execute(query)
		if commit:
			try:
				self.conn.commit()
			except sqlite3.OperationalError as e:
				print 'sqlite3 error:',e,query
			
	def select(self,query):
		c = self.conn.cursor()
		c.execute(query)
		return c.fetchall()
		
		
if __name__ == '__main__':
	assert not database.table_exists({'table_name':'rww'})
	assert database.table_exists({'table_name':'raw_temperature_measurements'})
