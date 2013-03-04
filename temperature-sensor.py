from serial import serial_reactor
from sensor import sensor

sensors = [
			sensor('Outside',0,-4.4),
			sensor('Kitchen',1,-1.2),
			sensor('Ceiling',2,-2.2),
			sensor('Study',3,-3.0),
			]


serial_reactor.run()