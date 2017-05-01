#-------------------------------main.py----------------------------------

#--------------------------------IMPORTS---------------------------------

import time, sys
sys.path.append('/home/pi/git/RPi-Files/outlet_box/relays')
sys.path.append('/home/pi/git/RPi-Files/outlet_box/sensors')
from Adafruit_IO import MQTTClient
from four_relays import four_relays
from ds18b20 import DS18B20

#--------------------------OUTLET VARIABLES------------------------------

Outlets = {'O1': {'pin': 19, 'type': 'none' , 'name': 'O1'         , 'state': 0, 't_change': 0},
           'O2': {'pin': 5 , 'type': 'none' , 'name': 'O2'         , 'state': 0, 't_change': 0},
           'O3': {'pin': 6 , 'type': 'light', 'name': 'desk light' , 'state': 0, 't_change': 0},
           'O4': {'pin': 13, 'type': 'light', 'name': 'room lights', 'state': 0, 't_change': 0}}

outlet_pins = (Outlets['O1']['pin'], Outlets['O2']['pin'], Outlets['O3']['pin'], Outlets['O4']['pin'])
outlet_names = (Outlets['O1']['name'], Outlets['O2']['name'], Outlets['O3']['name'], Outlets['O4']['name'])
outlet_types = (Outlets['O1']['type'], Outlets['O2']['type'], Outlets['O3']['type'], Outlets['O4']['type'])
print("Pins: {}, {}, {}, {}".format(outlet_pins[0], outlet_pins[1], outlet_pins[2], outlet_pins[3]))
print("Names: {}, {}, {}, {}".format(outlet_names[0], outlet_names[1], outlet_names[2], outlet_names[3]))
print("Types: {}, {}, {}, {}".format(outlet_types[0], outlet_types[1], outlet_types[2], outlet_types[3]))

#---------------------------OTHER VARIABLES------------------------------

# ADAFRUIT_IO dict with keys KEY and USERNAME
ADAFRUIT_IO = {'KEY': '11e4014862694ae6a474e89ece59c049', 'USERNAME': 'adavidson93'}
SUB_FEEDS = {'ifttt': 'IFTTT'}
PUB_FEEDS = {'temp':     'RoomTemp',
             'pressure': 'AirPressure',
             'light':    'AmbientLight',
             'pir':      'Motion',
             'altitude': 'Altitude'}
sample_rate = 10.0 #How often to send temperature value
room_temp = 10.0 #Initial value (could be anything....)

#-----------------------ADAFRUIT-IO CALLBACKS----------------------------

def connected(client):
    print("Connected to Adafruit IO!  Listening for {0} changes".format(SUB_FEEDS['ifttt']))
    client.subscribe(SUB_FEEDS['ifttt'])
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    print('payload[0:6] - {}'.format(payload[0:6]))
    if payload[0:6] in ('Outlet', 'outlet'):
        print('payload[-1] - {}, payload[-3:] - {}, payload[-4:] - {}'.format(payload[-1], payload[-3:], payload[-4:]))
        if (payload[-1] in ('1', '2', '3', '4')):
            if payload[-4:] == '1234':
                outlet_num = 'all'
            elif len(payload) == 7):
                outlet_num = int(payload[6])
            print('outlet_num: {}'.format(outlet_num))
            relays.flip(outlet_num)
        elif payload[-3:] in ('-ON', '-on', '-On'):
            outlet_num = int(payload[6]) if (len(payload) == 10) else 'all'
            print('outlet_num: {}'.format(outlet_num))
            relays.on(outlet_num)
        elif payload[-4:] in ('-OFF', '-off', '-Off'):
            outlet_num = int(payload[6]) if (len(payload) == 11) else 'all'
            print('outlet_num: {}'.format(outlet_num))
            relays.off(outlet_num)
    info = relays.receive_info_states()
    print('O1: {}, O2: {}, O3: {}, O4: {}'.format(info[0], info[1], info[2], info[3]))

#--------------------------------MAIN CODE-------------------------------

client = MQTTClient(ADAFRUIT_IO['USERNAME'], ADAFRUIT_IO['KEY'])
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()

relays = four_relays(outlet_pins, outlet_names, outlet_types)
ds = DS18B20('f', 2)
num_ds = ds.num_ds()
print('Number of DS18B20 sensors detected: {}'.format(num_ds))

last = 0
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
   #sensor_values = (ds.temp(), bmp.pressure(), bmp.altitude('ft'), bh.light('lux'), pir.motion(t_last_motion))
   client.loop()
   if (time.time() - last) >= sample_rate:
       room_temp = ds.temp()
       print('Publishing {0:.2f}F to RoomTemp feed.'.format(room_temp))
       client.publish(PUB_FEEDS['temp'], room_temp)
       last = time.time()

#------------------------------------------------------------------------
