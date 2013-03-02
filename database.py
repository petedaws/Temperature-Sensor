import sqlite3
import csv
import time
import datetime

class database:
	
	def __init__(self,db_path):
		self.conn = sqlite3.connect(db_path)
		
	def create_table(self,table_details):
		c = self.conn.cursor()
		columns = ','.join([' '.join([i[0],i[1]]) for i in table_details['columns']])
		c.execute('CREATE TABLE %s (%s)' % (table_details['table_name'],columns)
		self.conn.commit()