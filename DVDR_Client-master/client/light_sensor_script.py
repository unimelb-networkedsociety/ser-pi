# GrovePi+ & Grove Light Sensor & LED

import grovepi
 
# Connect the Grove Light Sensor to analog port A0
# SIG,NC,VCC,GND
 
# Connect the LED to digital port D4
# SIG,NC,VCC,GND
 
def read_sensor(light_sensor, threshold):
    grovepi.pinMode(light_sensor,"INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(light_sensor)
 
        # Calculate resistance of sensor in K
        if sensor_value>=0:
            resistance2 = (float)(1023 - sensor_value) * 10 / sensor_value 
            if resistance2 > threshold:
                # Send HIGH to switch on LED
                print "HIGH"
            else:
                # Send LOW to switch off LED
                print "LOW"
            print "sensor_value =", sensor_value, " resistance =", resistance2
            return [sensor_value, resistance2]
        else:
            sensor_value = 0
            resistance2 = 0
            return [sensor_value, resistance2]
    except IOError:
        print "Error"
