#!/usr/bin/env python
#
# GrovePi Example for using the Grove Light Sensor and the LED together to turn the LED On and OFF if the background light is greater than a threshold.
# Modules:
# 	http://www.seeedstudio.com/wiki/Grove_-_Light_Sensor
# 	http://www.seeedstudio.com/wiki/Grove_-_LED_Socket_Kit
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import time
import grovepi
import paho.mqtt.client as mqtt

# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
air_sensor = 0

#Sleep time
FREQ = 4

#Device Serial Number
CPUSERIAL = "0000000000000000"

#MQTT Server address
SERVER = '130.56.250.107'
#server = '10.110.110.150'
#server = '115.146.90.117'

#grovepi configuration
grovepi.pinMode(air_sensor, "INPUT")

sub_topic = '#' #subscribe all topics
pub_register = 'new device' #publish topic for device configuration




def read_value():
    """The method's docstring"""
    # Get sensor value
    sensor_value = grovepi.analogRead(air_sensor)
        #print("sensor_value =", sensor_value)
    return sensor_value

def air_condition(sensor_value):
    """The method's docstring"""
    if sensor_value > 700:
        return "High pollution"
    elif sensor_value > 300:
        return "Low pollution"
    else:
        return "Air fresh"

def on_connect(client, data, flags, rc):
    print 'Connect with the result code ' + str(rc)
    client.subscribe(sub_topic, 1)

def on_message(client, data, msg):	
        if msg.topic == 'config':
                global FREQ
                FREQ = float(msg.payload)
                print("The configuration has been changed for setting new sleep time as " + str(msg.payload) + " '")
        else:
                print("Receive message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos))

#get Raspberry pi serial number
def getserial():
        #Extract serial from CPUinfo file
        global CPUSERIAL
        try:
                #Read cpu file
                f = open('/proc/cpuinfo','r')
                for line in f:
                        #find out the serial info
                        if line[0:6] == 'Serial':
                                CPUSERIAL = line[10:26]
                f.close()
        except IOError:
                CPUSERIAL = "ERROR00000000000"
        return CPUSERIAL

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(SERVER, 1883, 60)
client.loop_start()

#set up serial number
myserial = getserial()
#client.publish(pub_register, myserial, 1)

#generate unique topic for air quality sensor
pub_air = myserial + ':Air_Quality:A0' 

while True:
    try:
        r = read_value()
        result = air_condition(r)
	client.publish(pub_air, "Air_qulity_SensorA0@Raspberry Pi No.1: Sensor_value = %d" % r, 1)
	#client.publish(pub_air, result, 1)
	print("time.sleep = " + str(FREQ))
        time.sleep(FREQ)

    except IOError:
        print ("Error")
