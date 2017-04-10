import sys
from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY      = ' '
ADAFRUIT_IO_USERNAME = 'adavidson93'

FEED_ID = 'IFTTT'

def connected(client):
    print('Connected to Adafruit IO. Listening for {0} changes...'.format(FEED_ID))
    client.subscribe(FEED_ID)

def disconnected(client):
    print('Disconnected from Adafruit IO')
    sys.exit(1)
    
def message(client, feed_id, payload):
    print('Feed {0} received new value {1}'.format(feed_id, payload)
    if payload=='outlet 1 on':
          print('Outlet-1 Turned ON via IFTTT')
    elif payload=='outlet 1 off':
          print('Outlet-1 Turned OFF via IFTT')
          
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
          
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
          
client.connect()
          
client.loop_blocking()
