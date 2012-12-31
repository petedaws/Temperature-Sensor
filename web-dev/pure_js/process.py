import csv
import time
import datetime
import json

csvrdr  = csv.reader(open('temp.csv','rb'))

s0 = []
s1 = []
s2 = []
s3 = []

for row in csvrdr:

	s = time.mktime(datetime.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S').timetuple())
	s0.append([(long(s)*1000),float(row[1])])
	s1.append([(long(s)*1000),float(row[2])])
	s2.append([(long(s)*1000),float(row[3])])
	s3.append([(long(s)*1000),float(row[4])])
	data = {'s0':s0,'s1':s1,'s2':s2}
	
open('temp_data.json','wb').write(json.dumps(data,indent=4))