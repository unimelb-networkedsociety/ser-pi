import grove_rtc
import time
grove_rtc.rtc_conf(2017,8,17,14,47,5,"thursday")
while True:
    try:
        # value = grove_rtc.rtc_getTime()
        # print "values: ", value
        time.sleep(2)
    except IOError:
        print "Error"

