#-------------------------------main.py----------------------------------

#--------------------------OUTLET VARIABLES------------------------------

Outlets = {'O1': {'pin': 19, 'name': 'O1', 'last': 0, 'new': -1},
           'O2': {'pin': 5, 'name': 'O2', 'last': 0, 'new': -1},
           'O3': {'pin': 6, 'name': 'desk light', 'last': 0, 'new': -1},
           'O4': {'pin': 13, 'name': 'room lights', 'last': 0, 'new': -1}}

outlet_pins = (Outlets['O1']['pin'], Outlets['O2']['pin'], Outlets['O3']['pin'], Outlets['O4']['pin'])
outlet_names = (Outlets['O1']['name'], Outlets['O2']['name'], Outlets['O3']['name'], Outlets['O4']['name'])

#---------------------------OTHER VARIABLES------------------------------

# ADAFRUIT_IO dict with keys KEY and USERNAME
ADAFRUIT_IO = {'KEY': '11e4014862694ae6a474e89ece59c049', 'USERNAME': 'adavidson93'}
SUB_FEED = 'IFTTT'
PUB_FEEDS = ('RoomTemp', 'AirPressure', 'AmbientLight', 'Motion', 'Altitude')
sample_rate = 10.0 #How often to send temperature value
room_temp = 10.0 #Initial value (could be anything....)

#--------------------------------IMPORTS---------------------------------

import time, sys
from Adafruit_IO import MQTTClient
from four_relays import four_relays
from ds18b20 import DS18B20
from bmp280 import BMP280

#-----------------------ADAFRUIT-IO CALLBACKS----------------------------

def connected(client):
    print("Connected to Adafruit IO!  Listening for {0} changes".format(SUB_FEED))
    client.subscribe(SUB_FEED)
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload[0:6] == 'Outlet':
        pin = payload[6]
        if payload[-3] == '-':
            function = payload[-2:]
        elif type(int(payload[-1])) == type(5):
            function = 'flip'
        if payload[-4:] = '1234':
            if function == 'ON':
                relays.on('all')
            elif function == 'OFF'
                relays.off('all')
            elif function == 'flip'
                relays.flip('all')
        else:
            pin = int(pin)
            if function == "ON":
                relays.on(pin)
            elif function == 'OFF'
                relays.off(pin)
            elif function == 'flip'
                relays.flip(pin)

    print('O1: {}, O2: {}, O3: {}, O4: {}'.format(relays.state('all')))

#--------------------------------MAIN CODE-------------------------------

client = MQTTClient(ADAFRUIT_IO['USERNAME'], ADAFRUIT_IO['KEY'])
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()

relays = four_relays(outlet_pins, outlet_names)
ds = DS18B20('f', 2)
num_ds = ds.device_count()
print('Number of DS18B20 sensors detected: {}'.format(num_ds))
#bmp = BMP280()

last = 0
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
   sensor_values = (ds.temp(), bmp.pressure(), bmp.altitude('ft'), bh.light('lux'), pir.motion(t_last_motion))
   ds,
   client.loop()
   if (time.time() - last) >= sample_rate:
       room_temp = read_temp()
       print('Publishing {0:.2f}F to RoomTemp feed.'.format(coffee_temp))
       client.publish(PUB_FEED, coffee_temp)
       last = time.time()

#------------------------------------------------------------------------
