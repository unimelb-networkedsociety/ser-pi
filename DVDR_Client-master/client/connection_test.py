import paho.mqtt.client as mqtt
import time
#MQTT Server address
server = '115.146.90.117'
#subscribe topic
pub_topic = 'test' #publish topic for device configuration
i = 0
def on_connect(client, data, flags, rc):
    client.subscribe("reply", 1)
    print 'Connect with the result code ' + str(rc)#return connection status
    #subscribe message from sensor
def on_message(client, data, msg):
    print 'new message received'
    print str(msg.payload)
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server, 1883, 60)
client.loop_start()
while True:
    try:
        i = i+1
        client.publish(pub_topic, i, 1)
        time.sleep(5)
    except IOError:
        print "Error"
    