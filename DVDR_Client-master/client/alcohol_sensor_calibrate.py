import time
import grovepi

analogInDatPin = 0
heaterSelPin = 15
sensorValue = 0
RS_air = 0
#grovepi.pinMode(heaterSelPin,&quot;OUTPUT&quot;)
grovepi.digitalWrite(heaterSelPin, 0)


#/*--- Get a average data by testing 100 times ---*/
for x in range(1,100):
    sensorValue = sensorValue +  grovepi.analogRead(analogInDatPin)
    time.sleep(0.1)
sensorValue = sensorValue/100.0
print("sensor value:")
print(sensorValue)
#/*-----------------------------------------------*/
sensor_volt = sensorValue/1024*5.0
RS_air = sensor_volt/(5.0-sensor_volt); #// omit *R16
print("sensor_volt = ")
print(sensor_volt)
print("V")
print("RS_air = ")
print(RS_air)