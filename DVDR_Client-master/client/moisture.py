import grovepi

# Connect the Grove Temperature & Humidity Sensor Pro to digital port D4
# SIG,NC,VCC,GND

def read_sensor(sensor_port):
    grovepi.pinMode(sensor_port,"INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(sensor_port)
 
        # Calculate resistance of sensor in K
        if sensor_value>=0:
            # resistance2 = (float)(1023 - sensor_value) * 10 / sensor_value 
            # if resistance2 > threshold:
            #     # Send HIGH to switch on LED
            #     print "HIGH"
            # else:
            #     # Send LOW to switch off LED
            #     print "LOW"
            # print "sensor_value =", sensor_value, " resistance =", resistance2
            return sensor_value
        else:
			sensor_value = 0
			return sensor_value
    except IOError:
        print "Error"