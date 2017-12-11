import time
import grovepi


#grovepi.pinMode(heaterSelPin,&quot;OUTPUT&quot;)
def read_sensor(): 
    try:
        analogInDatPin = 0
        heaterSelPin = 15
        sensorValue = 0
        RS_air = 0
        grovepi.digitalWrite(heaterSelPin, 0)
        time.sleep(0.1)
        #/*--- Get a average data by testing 100 times ---*/
        for x in range(1,100):
            sensorValue = sensorValue +  grovepi.analogRead(analogInDatPin)
        sensorValue = sensorValue/100.0
        sensor_volt = sensorValue/1024*5.0
        RS_gas = sensor_volt/(5.0-sensor_volt)
        #/*-Replace the name "R0" with the value of R0 in the demo of First Test -*/
        ratio = RS_gas/90.0222;  #// ratio = RS/R0
        #/*-----------------------------------------------------------------------*/
        print("sensor_volt = ")
        print(sensor_volt)
        print("V")
        print("RS_ratio = ")
        print(RS_gas)
        print("Rs/R0 = ");
        print(ratio)
        #--------------------
        grovepi.digitalWrite(heaterSelPin, 1)
        return [RS_gas, ratio]
    except IOError:
        print "Error"