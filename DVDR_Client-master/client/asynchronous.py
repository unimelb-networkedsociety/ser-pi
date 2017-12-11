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
import math
import time
import datetime
import grovepi
import paho.mqtt.client as mqtt
import threading
import multiprocessing
import xml.etree.ElementTree as ET
import os # Import the os library
import smbus
#rtc script
import grove_rtc
#import temperature and humidity python script 
import temp_hum
#import temperature and humidity python script for SHT31
import temp_hum2
#import air quiality pyhton script
import air_quality
#import moisture pyhton script
import moisture
#import ligth sensor python script
import light_sensor_script
#import color script
import color
#import ultrasonic script
import ultrasonic
#import compass script
import compass
#get device serial number
from GrovepiSerial import getserial
#check if internet is working 
from NetworkChecking import internet_on
from adxl345 import ADXL345
import time
#display serial number
#from SerialDisplay import serialDisplay


#----------------------------------------------------------------------------------------------------------------------
#---------------------------------------          Inital Configuration                     ----------------------------
#----------------------------------------------------------------------------------------------------------------------

#Process Pool
pool = []

# SIG,NC,VCC,GND
#air_sensor = 0                  # Connect the Grove Air Sensor to analog port A0
#dht_sensor_port = 8		 # Connect the DHt sensor to port 8

#Display serial number on LCD
#serialDisplay()

#set up serial number
myserial = getserial()

#inital xml configuration file
global root
global tasklist
global et
try:
    #read the configration file
    et = ET.parse('config.xml')
    #set up root for device config info
    root = et.getroot()
    #set up task element for task info
    tasklist = root.find('tasklist')
    #the flag that if the device has been registered
    register_flag = root.find('register_flag').text
    #Enrolemnt Id
    enrolment_id = root.find('enrolment_id').text
except ImportError:
    print "Import Error"

#MQTT Server address
file_open = open("ipaddress.txt", "r") #opens file with name of "test.txt"
server = file_open.read()
server = server.strip(' \t\n\r')
print server
file_open.close()
# server = '35.189.4.239' #server = '115.146.90.117'

#subscribe topic
pub_register = 'new device' #publish topic for device configuration


#----------------------------------------------------------------------------------------------------------------------
#---------------------------------------          Sensor function                     ---------------------------------
#----------------------------------------------------------------------------------------------------------------------

def color_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            color_port = int(port[1])
                        #grovepi configuration
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            data = color.read_sensor()
            ###generate unique topic for air quality sensor
            #pub_air = myserial+':'+tsk_id+':'+port
            #topicdevi
            pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name

            #client.publish(pub_topic, "%s@%s" % (data, datetime.datetime.now()), 1)
            client.publish(pub_topic, "%s@%s" % (data, datetime.datetime.now()), 1)
            time.sleep(frequence)

        except IOError:
            print "Error"

def moisture_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            moisture_port = int(port[1])
                        #grovepi configuration
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            data = moisture.read_sensor(moisture_port)
            ###generate unique topic for air quality sensor
            #pub_air = myserial+':'+tsk_id+':'+port
            #topic
            pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name
            #client.publish(pub_topic, "%s@%s" % (data, datetime.datetime.now()), 1)
            client.publish(pub_topic, "%.2f@%s" % (data, datetime.datetime.now()), 1)
            time.sleep(frequence)

        except IOError:
            print "Error"

def air_quality_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            air_sensor = int(port[1])
                        #grovepi configuration
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            r = air_quality.read_sensor(air_sensor)
            ###generate unique topic for air quality sensor
            #pub_air = myserial+':'+tsk_id+':'+port
            #topic
            pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name
            client.publish(pub_topic, "%s@%s" % (r, datetime.datetime.now()), 1)
            time.sleep(frequence)

        except IOError:
            print "Error"

def temperature_humidity_sensor2(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            dht_sensor_port = int(port[1])
                        # Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
                        #  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
                        #  1 - DHT22 - white one, aka DHT Pro or AM2302
                        #  2 - DHT21 - black one, aka AM2301
            dht_sensor_type = 0
            client = mqtt.Client()
            client.connect(server, 1883, 60)
                        #sensor config and value read
            print 'temperature2-1:'
            [temp, hum] = temp_hum2.read_sensor()
            print 'temperature2-2:'
            print [temp, hum]
            if math.isnan(temp) or temp==-1:#check if temp is nan, if it is then don't publish
                print 'not a number'
            else:
                print 'temperature2-3:'
							#setup topic for temperature&humidity sensor
                #pub_temp = myserial + ':' + tsk_id +':' + port
                #pub_temp = myserial + ':' + port# enrolment Id : myseria:sensortype:sensorname
                pub_temp = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name# enrolment Id : myseria:sensortype:sensorname
                print 'temperature2-4:'
		#public the message
                #client.publish(pub_temp, "%s@%s" % (round(Decimal(temp,2)), datetime.datetime.now()), 1)
                client.publish(pub_temp, "%s@%s" % (temp, datetime.datetime.now()), 1)
                print 'temperature2-5:'
                time.sleep(frequence)
                print 'temperature2-6:'
        except (IOError, TypeError) as e:
            print "Error"
            print IOError
            print TypeError


def temperature_humidity_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            dht_sensor_port = int(port[1])
                        # Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
                        #  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
                        #  1 - DHT22 - white one, aka DHT Pro or AM2302
                        #  2 - DHT21 - black one, aka AM2301
            dht_sensor_type = 0 #check here if sensorname can be used to identify the sensor type.
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            print 'Humidity2-1:'
            print 'port:', dht_sensor_port
            [temp, hum] = temp_hum.read_sensor(dht_sensor_port, dht_sensor_type)
            print "temperature:", temp
            print "humidity", hum
            print 'Humidity2:'
            if math.isnan(temp) or temp==-1:#check if temp is nan, if it is then don't publish
                print 'not a number'
            else:
							#setup topic for temperature&humidity sensor
                #pub_temp = myserial + ':' + tsk_id +':' + port
                #pub_temp = myserial + ':' + port# enrolment Id : myseria:sensortype:sensorname
                pub_temp = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name# enrolment Id : myseria:sensortype:sensorname
		#public the message

                client.publish(pub_temp, "%s@%s" % (temp, datetime.datetime.now()), 1)
                time.sleep(frequence)
        except (IOError, TypeError) as e:
            print "Error"

def humidity_sensor2(frequence, port, tsk_id, enrollment, sensor, sensor_name):
     while True:
        try:
                        #format port
            dht_sensor_port = int(port[1])
                        # Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
                        #  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
                        #  1 - DHT22 - white one, aka DHT Pro or AM2302
                        #  2 - DHT21 - black one, aka AM2301
            dht_sensor_type = 0
            client = mqtt.Client()
            client.connect(server, 1883, 60)
                        #sensor config and value read
            print 'humidity-1:'
            [temp, hum] = temp_hum2.read_sensor()
            print 'humidity-2:'
            if math.isnan(hum) or hum==-1:#check if temp is nan, if it is then don't publish
                print 'not a number'
            else:
                print 'humidity-3:'
							#setup topic for temperature&humidity sensor
                #pub_temp = myserial + ':' + tsk_id +':' + port
                #pub_temp = myserial + ':' + port# enrolment Id : myseria:sensortype:sensorname
                pub_hum = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name# enrolment Id : myseria:sensortype:sensorname
                print 'humidity-4:'
		#public the message
                #client.publish(pub_temp, "%s@%s" % (round(Decimal(temp,2)), datetime.datetime.now()), 1)
                client.publish(pub_hum, "%s@%s" % (hum, datetime.datetime.now()), 1)
                print 'humidity-5:'
                time.sleep(frequence)
                print 'humidity-6:'
        except (IOError, TypeError) as e:
            print "Error"
            print IOError
            print TypeError
        

def humidity_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            dht_sensor_port = int(port[1])
                        # Note the dht_sensor_type below may need to be changed depending on which DHT sensor you have:
                        #  0 - DHT11 - blue one - comes with the GrovePi+ Starter Kit
                        #  1 - DHT22 - white one, aka DHT Pro or AM2302
                        #  2 - DHT21 - black one, aka AM2301
            dht_sensor_type = 0 #check here if sensorname can be used to identify the sensor type.
            client = mqtt.Client()
            client.connect(server, 1883, 60)
                        #sensor config and value read
            [temp, hum] = temp_hum.read_sensor(dht_sensor_port, dht_sensor_type)
            if math.isnan(hum):#check if temp is nan, if it is then don't publish
                print 'not a number'
            else:
							#setup topic for temperature&humidity sensor
                #pub_temp = myserial + ':' + tsk_id +':' + port
                #pub_temp = myserial + ':' + port# enrolment Id : myseria:sensortype:sensorname
                pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name#
		#public the message
                client.publish(pub_topic, "%s@%s" % (hum, datetime.datetime.now()), 1)
                time.sleep(frequence)
        except (IOError, TypeError) as e:
            print "Error"


def light_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            light_sensor = int(port[1])
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            [sensor_value, Resistance] = light_sensor_script.read_sensor(light_sensor, 10)
            if sensor_value != 0:
                #setup the topic
                #pub_light = myserial + ':' + tsk_id  + ':' + port
                pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name#
                #public message
                client.publish(pub_topic, "%s@%s" % (sensor_value, datetime.datetime.now()), 1)
                time.sleep(frequence)
        except (IOError, TypeError) as e:
            print "Error"

def compass1(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    print 'frequence:'
    print frequence
    while True:
        try:
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            value = compass.read_sensor()
            #time.sleep(2)
                #setup the topic
                #pub_light = myserial + ':' + tsk_id  + ':' + port
            pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name#
            #public message
            client.publish(pub_topic, "%s@%s" % (value, datetime.datetime.now()), 1)
            time.sleep(frequence)
        except (IOError, TypeError) as e:
            print "Error"
def ultrasonic_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
                        #format port
            sensor_port = int(port[1])
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            sensor_value = ultrasonic.read_sensor(sensor_port)
            if sensor_value != 0:
                #setup the topic
                #pub_light = myserial + ':' + tsk_id  + ':' + port
                pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name#
                #public message
                client.publish(pub_topic, "%s@%s" % (sensor_value, datetime.datetime.now()), 1)
                time.sleep(frequence)
        except (IOError, TypeError) as e:
            print "Error"    
def accelerometer_sensor(frequence, port, tsk_id, enrollment, sensor, sensor_name):
    while True:
        try:
            adxl345 = ADXL345()
            client = mqtt.Client()
            client.connect(server, 1883, 60)
            # sensor_value = ultrasonic.read_sensor(sensor_port)

            axes = adxl345.getAxes(True)
	        # print(( axes['x'] ),"\t",( axes['y'] ),"\t",( axes['z'] ))

            # if sensor_value != 0:
                #setup the topic
                #pub_light = myserial + ':' + tsk_id  + ':' + port
            pub_topic = enrollment + ':' + myserial + ':' + sensor + ':' + sensor_name#
                #public message
            client.publish(pub_topic, "%s@%s" % (axes, datetime.datetime.now()), 1)
            time.sleep(frequence)
        except (IOError, TypeError) as e:
            print "Error" 

#----------------------------------------------------------------------------------------------------------------------
#---------------------------------------          Process Manager                     ---------------------------------
#----------------------------------------------------------------------------------------------------------------------
def createtsk(target, tsk_freq, tsk_port, tsk_id, enrollment, sensor, sensor_name):
    #start the corresponding function as process
    thr = multiprocessing.Process(target = target, args=(float(tsk_freq), tsk_port, tsk_id, enrollment, sensor, sensor_name))#create the thread to run the corresponding sensor function
    thr.start()
    #append the process into process pool
    pool.append((tsk_id, thr))

def stoptsk(tsk_id):
    #iterate to find exsisted process
    for Key, Value in pool:
        if Key == tsk_id:
            #kill the process and remove from pool
            Value.terminate()
            pool.remove((Key, Value))

def updatetsk(target, tsk_freq, tsk_port, tsk_id, enrollment, sensor, sensor_name):
    #iterate to find exsisted process
    for Key, Value in pool:
        if(Key == tsk_id):
            #kill the process and remove from pool
            Value.terminate()
            pool.remove((Key,Value))
    #start the corresponding function as process
    thr = multiprocessing.Process(target = target, args=(float(tsk_freq),tsk_port,tsk_id, enrollment, sensor, sensor_name))      #create the thread to run the corresponding sensor function
    thr.start()
    #append the process into process pool
    pool.append((tsk_id, thr))

def taskCreated(task_id):
    print 'Task Created?'
    x = 0
    tasks = tasklist.findall('task')
    for task in tasks:
        if task.find('name').text == task_id:
            x = x + 1
    if x == 0:
        return False
    else:
        return True
#action filter to take different actions
def tskAction(function, action, set_sensor, set_fre, set_port, set_enroll, set_tskid, sensor_name):
    if action == 'start':
        print 'start action'
        if taskCreated(set_tskid) == False:
            print 'new task added'
            Add_new_tsk(set_tskid, set_sensor, 'stop', set_fre, set_port, set_enroll, sensor_name)
        print 'starting task'
        #tasks = tasklist.findall('task')
        for task in tasklist:
            if task.find('name').text == set_tskid:
                print 'tsk id matched'
                createtsk(function, set_fre, set_port, set_tskid, set_enroll, set_sensor, sensor_name)
        Change_state(set_tskid, 'start')

    elif(action == 'add'):
        print 'add task action'
        # print taskCreated(set_tskid)
        if taskCreated(set_tskid) == False:
            print 'new task added'
            Add_new_tsk(set_tskid, set_sensor, 'stop', set_fre, set_port, set_enroll, sensor_name)
        else:
            print 'task aready exist.'

    elif action == 'stop':
        print 'stop task action'
        if taskCreated(set_tskid) == False:
            print 'new task added'
            Add_new_tsk(set_tskid, set_sensor, 'stop', set_fre, set_port, set_enroll, sensor_name)
        else:
            print 'task aready exist.'
            #delete the thread
            stoptsk(set_tskid)
            Change_state(set_tskid, 'stop')

    elif action == 'restart':
        #restart stop task
        print 'restart task action'
        for task in tasklist:
            if task.get('name').text == set_tskid:
                createtsk(function, set_fre, set_port, set_tskid, set_enroll, set_sensor, sensor_name)
        Change_state(set_tskid, 'start')

    elif action == 'delete':
        print 'delete task action'
        if taskCreated(set_tskid) == True:
            #delete the thread and delete task info in xml
            print 'deleting task'
            tasks = tasklist.findall('task')
            print 'tasks:'
            print tasks
            for task in tasks:
                print 'task:'
                print task
                if task.find('name').text == set_tskid:
                    if task.find('status').text != 'stop':
                        print 'differen from stop'
                        stoptsk(task.find('name').text)
                    Remove_tsk(task.find('name').text)
            # for task in tasklist:
            #         if task.get('name') == set_tskid:
            #                 if task.find('status').text != 'stop':
            #                         stoptsk(set_tskid)
            # Remove_tsk(set_tskid)

    elif action == 'update':
        print 'update task actions'
        if taskCreated(set_tskid) == False:
            print 'new task added'
            Add_new_tsk(set_tskid, set_sensor, 'stop', set_fre, set_port, set_enroll, sensor_name)
        #update the thread and update the xml config file
        print 'frequency has been updated'
        for task in tasklist:
            if task.find('name').text == set_tskid:
                if task.find('status').text != 'stop':
                    print 'task start and update'
                    updatetsk(function, set_fre, set_port, set_tskid, set_enroll, set_sensor, sensor_name)
                    Remove_tsk(set_tskid)
                    Add_new_tsk(set_tskid, set_sensor, task.find('status').text, set_fre, set_port, set_enroll, sensor_name)
                else:
                    print 'task stop and update'
                    Change_tsk(set_tskid, set_fre, set_port)

#filter different sensor
def whichTask(sensor, status, frequency, port, enrollment, tsk_id, sensor_name):
    print 'sensor:'
    print sensor
    if sensor == 'Air quality':
        tskAction(air_quality_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Temperature':
        tskAction(temperature_humidity_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'TemperatureSHT31':
        print 'Task Temperature SHT31'
        tskAction(temperature_humidity_sensor2, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Moisture':
        print 'Moisture'
        tskAction(moisture_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Color':
        print 'Color'
        tskAction(color_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Humidity':
        tskAction(humidity_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)
    
    elif sensor == 'HumiditySHT31':
        print 'Task Humidity SHT31'
        tskAction(humidity_sensor2, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Light':
        tskAction(light_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Compass':
        tskAction(compass1, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)
    
    elif sensor == 'Ultrasonic':
        tskAction(ultrasonic_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    elif sensor == 'Accelerometer':
        tskAction(accelerometer_sensor, status, sensor, frequency, port, enrollment, tsk_id, sensor_name)

    else:
        print 'no corresponding task on client'

#----------------------------------------------------------------------------------------------------------------------
#---------------------------------------               XML                      ---------------------------------------
#----------------------------------------------------------------------------------------------------------------------
#this function is used to modified the xml config file by adding new task info
def Add_new_tsk(tsk_name, sensor, status, frequency, port, enrollment, sensor_name):
    tsk = ET.SubElement(tasklist, "task")
    tsk_sensor = ET.SubElement(tsk, "name")
    tsk_sensor.text = tsk_name
    tsk_sensor = ET.SubElement(tsk, "sensor")
    tsk_sensor.text = sensor
    tsk_status = ET.SubElement(tsk, "status")
    tsk_status.text = status
    tsk_frequence = ET.SubElement(tsk, "frequency")
    tsk_frequence.text = frequency
    tsk_port = ET.SubElement(tsk, "port")
    tsk_port.text = port
    tsk_enrollment = ET.SubElement(tsk, "enrollment")
    tsk_enrollment.text = enrollment
    tsk_enrollment = ET.SubElement(tsk, "sensor_name")
    tsk_enrollment.text = sensor_name
    ET.dump(tasklist)
    et.write('config.xml')

#remove the task info from xml file
def Remove_tsk(tsk_name):
    for task in tasklist:
        if task.find('name').text == tsk_name:
            tasklist.remove(task)
    et.write('config.xml')

#change the state of task
def Change_state(tsk_name, status):
    for task in tasklist:
        if task.find('name').text == tsk_name:
            task.find('status').text = status
    et.write('config.xml')

#change parameter of task
def Change_tsk(tsk_name, frequency, port):
    for task in tasklist:
        if task.find('name').text == tsk_name:
            task.find('frequency').text = frequency
            task.find('port').text = port
    et.write('config.xml')

#----------------------------------------------------------------------------------------------------------------------
#---------------------------------------               MQTT                     ---------------------------------------
#----------------------------------------------------------------------------------------------------------------------
def on_connect(client, data, flags, rc):
    print 'Connect with the result code ' + str(rc)#return connection status
    #subscribe message from sensor
    client.subscribe(str(myserial)+":"+"task", 1)#Only subscribe to these topics
    client.subscribe(str(myserial)+":"+"device", 1)
    client.subscribe(str(myserial)+":"+"init", 1)

def on_message(client, data, msg):
    device = str(msg.topic).split(':')[0]
    print str(msg.topic)
    if device == myserial:
        topic = str(msg.topic).split(':')[1]
        if topic == 'task':
            global frequence
            #phrase the message for task(may become a independent function)
            info = str(msg.payload).split(':')
            print str(msg.payload)
            # sensor = info[0];
            # status = info[1];
            # frequency = info[2];
            # port = info[3]
            # enrollment = info[4]
            # tsk_id = info[5];
            # sensor_name = info[3];
            enrollment = info[0]
            sensor = info[2]
            sensor_name = info[3]
            port = info[4]
            frequency = info[5]
            status = info[6]
            tsk_id = info[7]
            command_id = info[8] #ack
            #check the output
            print "sensor:" + sensor + " status:" + status + " frequency:" + frequency + " port:" + port + " enrollment:" + enrollment + " tsk id:" + tsk_id
            #enrolementID doesnot match reply with warning message
            global enrolment_id
            if enrolment_id != enrollment:
                print 'different enrolements ID'
                #topic: Error
                #message: enrolment id:myserial:ackID
                #check which task to do
                client.publish(enrolment_id+':'+myserial+':'+command_id, 'Error', 1)#Ack
            else:
                print 'equal enrolment ids'
                client.publish('ack', myserial + ':' + command_id, 1)#Ack
                whichTask(sensor, status, frequency, port, enrollment, tsk_id, sensor_name)

        elif topic == 'device':
            print "device topic"
            global register_flag
            print "message:"
            print str(msg.payload)
            global register_flag
            #filter different device action
            if str(msg.payload) == "record":
                #the device serial number has been stored into unregistered_device db and change the flag into true
                print "device has been detected"
                register_flag = True
                root.find('register_flag').text = "True"
                et.write('config.xml')
                print "register flag:"
                print root.find('register_flag').text

            elif str(msg.payload) == "unregistered":
                #the device serial number has been deleted from registered_device db and change the flag into False
                print "device has been unregistered"
                register_flag = False
                root.find('register_flag').text = "False"
                et.write('config.xml')
            else:
                print 'device config fail'
        elif topic == 'init':
            global enrolment_id#ack:enrolementID
            print 'init topic'
            info = str(msg.payload).split(':')
            enrolment_id = info[1] # enrolment ID
            root.find('enrolment_id').text = enrolment_id
            #delete the thread and delete task info in xml
            # for task in tasklist:
            #         if task.find('status').text != 'stop':
            #                 stoptsk()
            # Remove_tsk(set_tskid)
            print 'lenght'
            print len(tasklist)
            tasks = tasklist.findall('task')
            print 'tasks:'
            print tasks
            for task in tasks:
                print 'task:'
                print task
                if task.find('status').text != 'stop':
                    print 'differen from stop'
                    stoptsk(task.find('name').text)
                Remove_tsk(task.find('name').text)
            # for elem in tasklist.iter():
            #         print elem
            #         if elem.find('status') != 'stop':
            #                print 'differen from stop'
            #                stoptsk(elem.find('name'))
            #         Remove_tsk(elem.find('name'))
            for Key, Value in pool:
                #kill the process and remove from pool
                Value.terminate()
                pool.remove((Key, Value))
                #Delete every task from the task tasklist
                #delete the thread and delete task info in xml
            et.write('config.xml')
            client.publish('ack', myserial + ':' + info[0], 1)#Ack
        else:
            print "Receive message '" + str(msg.payload) + "' on topic '" + msg.topic + "' with QoS " + str(msg.qos)


while True:
    if internet_on():
        print 'Wifi has been connected'
        break
    else:
        print 'Wifi has not been connected'
    time.sleep(5)

bus = smbus.SMBus(1)

try:
    bus.write_byte(0x68, 0x00)
    #get time from RTC
    value = grove_rtc.rtc_getTime()

    year = '%02d' % value[0]
    year = "20"+str(year)
    print "values: ", year
    #month = str(value[1])
    month = '%02d' % value[1]
    #day = str(value[2])
    day = '%02d' % value[2]

    hour = '%02d' % value[3]

    minutes = '%02d' % value[4]

    real_time = year+month+day+" "+hour+minutes

    print "print time:", real_time

    command ="sudo date --set='"+real_time+"'"

    print "print command:", command


    os.system(command)
except: # exception if read_byte fails
    print "RTC NOT available"

print "rpi time:", datetime.datetime.now()
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(server, 1883, 60)
client.loop_start()
client.publish('register',  myserial, 1)



#restart all the interrupted task
##tasks = tasklist.findall('task')
for task in tasklist:
    if task.find('status').text == 'start':
        print 'sensor:'
        print task.find('sensor').text
        print 'frequency:'
        print task.find('frequency').text
        print 'port:'
        print task.find('port').text
        print 'enrollment:'
        print task.find('enrollment').text
        print 'name:'
        print task.find('name').text
        print 'sensor_name:'
        print task.find('sensor_name').text
        whichTask(task.find('sensor').text, 'start', task.find('frequency').text, task.find('port').text, task.find('enrollment').text, task.find('name').text, task.find('sensor_name').text)


#---------------------------------------
def greeting():
    client.publish('greeting', myserial, 1)
#-----------------------------------------    Main loop         -----------------------------------------------
greeting()
while True:
    try:
        time.sleep(10)
        #if flag is false then keep sending greeting message every ten second
        if register_flag == False:
            client.publish('register', myserial, 1)
    except (IOError, TypeError) as e:
        print "Error"
