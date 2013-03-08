#TODO:
# 1) Make the code agnostic to the number of sensors

import sqlite3
import time
from database import Database


def migrate(from_db,to_db):
	table = 'raw_temperature_measurements'
	results = from_db.select('SELECT * from %s' % (table))
	to_db.create_table({'table_name':'Outside_raw','table_columns':[('date','integer'),('value','float')]})
	to_db.create_table({'table_name':'Kitchen_raw','table_columns':[('date','integer'),('value','float')]})
	to_db.create_table({'table_name':'Ceiling_raw','table_columns':[('date','integer'),('value','float')]})
	to_db.create_table({'table_name':'Study_raw','table_columns':[('date','integer'),('value','float')]})
	for result in results:
		to_db.add_record({'table_name':'Outside_raw','values':(result[0],result[1])},commit=False)
		to_db.add_record({'table_name':'Kitchen_raw','values':(result[0],result[2])},commit=False)
		to_db.add_record({'table_name':'Ceiling_raw','values':(result[0],result[3])},commit=False)
		to_db.add_record({'table_name':'Study_raw','values':(result[0],result[4])},commit=False)


def init():
	t = time.localtime()
	tm = time.strftime('%Y-%m-%d_%H-%M-%S',t)
	db_from = Database('temp.db')
	db_to = Database('output_%s.db'%(tm))
	migrate(db_from,db_to)
	db_to.conn.commit()
	db_to.conn.close()
	db_from.conn.close()

if __name__ == "__main__":
	init()