import temp_hum
import time
# grove_rtc.rtc_conf(2017,7,6,12,28,5,"thursday")
while True:
    try:
        value = temp_hum.read_sensor(3, 0)
        print "values: ", value
        time.sleep(2)
    except IOError:
        print "Error"

