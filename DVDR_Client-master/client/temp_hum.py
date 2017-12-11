from grovepi import *

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# SIG,NC,VCC,GND

def read_sensor(dht_sensor_port,dht_sensor_type): 
	try:
		[ temp,hum ] = dht(dht_sensor_port,dht_sensor_type)		#Get the temperature and Humidity from the DHT sensor
		return [temp,hum]
	except IOError:
		print "Error"