# GrovePi + Grove Ultrasonic Ranger
from grovepi import *
 # Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
 # ultrasonic_ranger = 4
def read_sensor(sensor_port): 
    try:
        # Read distance value from Ultrasonic
        sensor_value=ultrasonicRead(sensor_port)
        return sensor_value
    except TypeError:
        print "Error"
    except IOError:
        print "Error"