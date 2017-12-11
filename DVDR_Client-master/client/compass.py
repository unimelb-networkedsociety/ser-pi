import grove_compass_lib
import time
def read_sensor(): 
    c=grove_compass_lib.compass()
    print("X:",c.x,"Y:",c.y,"X:",c.z,"Heading:",c.headingDegrees)
    c.update()
    time.sleep(0.1)
    return [c.x,c.y,c.z,c.headingDegrees]