import grovepi

# Connect the Grove Air Quality Sensor to analog port A0
# SIG,NC,VCC,GND

def read_sensor(air_sensor):
    grovepi.pinMode(air_sensor, "INPUT")
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(air_sensor)

        if sensor_value > 700:
            print "High pollution"
        elif sensor_value > 300:
            print "Low pollution"
        else:
            print "Air fresh"

        print "sensor_value =", sensor_value
        return sensor_value

    except IOError:
        print "Error"
        