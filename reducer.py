import sqlite3
import csv
import time
import datetime

# The reducer is a filter through which database transactions are indexed for efficient retrieval
# Data should be stored in the database as a timestamp and BLOB. To get the blob we could 
# conceivably pass a list of functions that will applied sequentially to a block of data.
# The database row would be {'timestamp':123123,'data':{'max':12,'min':31,'start':12,'end':12}}
# but each row could be different. This way we know that if we want data from a particular "master"
# (each sensor will have its own "master" or "raw" table) table at a particular resolution, we just need
# to pull down data from the table that provides the correct resolution. Allowable resolutions will
# probably need to be known up-front since we need to know what table to query to get the expected resolution
# for a given range.

class reducer:
	
	def __init__(self):
		None #TODO
		
	def add_data(self):
		None #TODO
		
	def get_data(self):
		None #TODO