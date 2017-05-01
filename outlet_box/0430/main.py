#-------------------------------main.py----------------------------------

#--------------------------------IMPORTS---------------------------------

import time, sys
sys.path.append('/home/pi/git/RPi-Files/outlet_box/relays')
sys.path.append('/home/pi/git/RPi-Files/outlet_box/sensors')
sys.path.append('/home/pi/git/RPi-Files/outlet_box/0430')
from Adafruit_IO import MQTTClient
from four_relays import four_relays
from type_test import type_test
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

def payload_seperator(payload):
    payload_d = {'num_sections': 0}
    num_sec = payload.count(',') + 1
    payload_d['num_sections'] = num_sec
    if num_sec == 1:
        payload_d['sec1'] = payload[:]
    elif num_sec in [2, 3, 4]:
        comma1 = payload.index(',')
        payload_d['sec1'] = payload[0:comma1]
        payload_rem = payload[comma1+1:]
        if num_sec in [3, 4]:
            comma2 = payload_rem.index(',')
            payload_d['sec2'] = payload[comma1:comma2]
            payload_rem = payload[comma2+1:]
            if num_sec == 4:
                comma3 = payload.index(',')
                payload_d['sec3'] = payload[comma2:comma3]
                payload_d['sec4'] = payload[comma3:]
            else:
                payload_d['sec3'] = payload[comma2:]
        else:
            payload_d['sec2'] = payload[comma1:]
    else:
        print('num_sec is out of range. Must be between 1,4')
    return payload_d

def outlet_manager(payload_d):
    addr = payload_d['sec2']
    if addr in ('ALL', 'All', 'all', '*', 'a', ':', '1234', 1234):
        outlet_addr = 'all'
    elif addr in (1, 2, 3, 4, '1', '2', '3', '4'):
        outlet_addr = int(addr)
    elif addr in outlet_names:
        outlet_addr = addr
    else:
        outlet_addr = 'all'
        print('outlet address outside of range (1/2/3/4/*), using default-->(all)')
    if (payload_d['num_sections'] in [3,4]):
        func = payload_d['sec3']
        if func in ('ON', 'On', 'on', 1, '1', 'HIGH', 'high', 'True', True):
            relays.on(outlet_addr)
        elif func in ('OFF', 'Off', 'off', 0, '0', 'LOW', 'low', 'False', 'False'):
            relays.off(outlet_addr)
        elif func in ('FLIP', 'Flip', 'flip', -1, '-1', 'opposite', 'switch'):
            relays.flip(outlet_addr)
    else:
        relays.flip(outlet_addr)

def connected(client):
    print("Connected to Adafruit IO!  Listening for {0} changes".format(SUB_FEEDS['ifttt']))
    client.subscribe(SUB_FEEDS['ifttt'])
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    payload_d = payload_seperator(payload)
    num_sec = payload_d['num_sections']
    if payload_d['sec1'] in ('Outlet', 'outlet', 'Outlets', 'outlets', 'Out', 'out', 'O') and (num_sec > 1):
        outlet_manager(payload_d)
        info = relays.retrieve_info_states()
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
