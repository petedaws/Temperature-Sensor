from serialport import Serial_Reactor
from sensor import Sensor
from database import Database

if __name__ == '__main__':
	db = Database('temp.db')
	
	sensors = [
			Sensor('Outside',0,-4.4,db),
			Sensor('Kitchen',1,-1.2,db),
			Sensor('Ceiling',2,-2.2,db),
			Sensor('Study',3,-3.0,db),
			]
	
	
	if platform.system() == 'Windows':
		serial_reactor = Serial_Reactor('COM7',300)
	else:
		serial_reactor = Serial_Reactor('/dev/ttyUSB0',300)
	
	for sens in sensors:
		serial_reactor.connect_event('sensor_reading',sens.add_record)
	
	serial_reactor.run()