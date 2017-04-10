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
  
