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
class variables:
    def __init__(self):
        self.Outlets = {'O1': {'pin': 19, 'type': 'none' , 'name': 'O1'         , 'state': 0, 't_change': 0},
                        'O2': {'pin': 5 , 'type': 'none' , 'name': 'O2'         , 'state': 0, 't_change': 0},
                        'O3': {'pin': 6 , 'type': 'light', 'name': 'desk light' , 'state': 0, 't_change': 0},
                        'O4': {'pin': 13, 'type': 'light', 'name': 'room lights', 'state': 0, 't_change': 0}}
        self.outlet_pins = (Outlets['O1']['pin'], Outlets['O2']['pin'], Outlets['O3']['pin'], Outlets['O4']['pin'])
        self.outlet_names = (Outlets['O1']['name'], Outlets['O2']['name'], Outlets['O3']['name'], Outlets['O4']['name'])
        self.outlet_types = (Outlets['O1']['type'], Outlets['O2']['type'], Outlets['O3']['type'], Outlets['O4']['type'])
        print("Pins: {}, {}, {}, {}".format(outlet_pins[0], outlet_pins[1], outlet_pins[2], outlet_pins[3]))
        print("Names: {}, {}, {}, {}".format(outlet_names[0], outlet_names[1], outlet_names[2], outlet_names[3]))
        print("Types: {}, {}, {}, {}".format(outlet_types[0], outlet_types[1], outlet_types[2], outlet_types[3]))
        self.ADAFRUIT_IO
        self.SUB_FEEDS
        self.PUB_FEEDS
        self.t_rate = 10.0
        self.room_temp = -1
        self.relays = four_relays(var.outlet_pins, var.outlet_names, var.outlet_types)
        self.ds = DS18B20('f', 2)
        self.num_ds = ds.num_ds()
        self.ADAFRUIT_IO = {'KEY': '11e4014862694ae6a474e89ece59c049', 'USERNAME': 'adavidson93'}
        self.SUB_FEEDS = {'ifttt': 'IFTTT'}
        self.PUB_FEEDS = {'temp':     'RoomTemp',
                     'pressure': 'AirPressure',
                     'light':    'AmbientLight',
                     'pir':      'Motion',
                     'altitude': 'Altitude'}
        self.sample_rate = 10.0 #How often to send temperature value
        self.room_temp = 10.0 #Initial value (could be anything....)
        self.last = 0
#---------------------------OTHER VARIABLES------------------------------

# ADAFRUIT_IO dict with keys KEY and USERNAME


#-----------------------ADAFRUIT-IO CALLBACKS----------------------------

def payload_seperator(payload, seperator=','):
    n_sect = payload.count(sep) + 1
    sections = [x.strip() for x in payload.split(seperator)]
    sect_range = range(len(sections))
    sect_names = ['sect{}'.format(i+1) for i in sect_range]
    sect_values = [sections[i] for i in sect_range]
    payload_dict = dict(((sect_names[i], sect_values[i]) for i in sect_range) + ('n_sect', n_sect))
    for i in sect_range:
        print("name->('{}'), value->('{}'), payload_dict[name]->()". format(sect_names[i], sect_values[i], payload_dict[sect_names[i]]))
    if n_sect > 4:
        print('n_sect is out of range (currenly: {}). Must be between 1,4'.format(n_sect))
    return payload_dict

def outlet_manager(payload_dict):
    addr = payload_dict['sec2']
    if addr in ('ALL', 'All', 'all', '*', 'a', ':', '1234', 1234):
        outlet_addr = 'all'
    elif addr in (1, 2, 3, 4, '1', '2', '3', '4'):
        outlet_addr = int(addr)
    elif addr in outlet_names:
        outlet_addr = addr
    else:
        outlet_addr = 'all'
        print('outlet address outside of range (1/2/3/4/*), using default-->(all)')
    if (payload_dict['n_sect'] in [3,4]):
        func = payload_dict['sec3']
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
    payload_dict = payload_seperator(payload, seperator=',')
    n_sect = payload_dict['n_sect']
    print('payload_dict.items() -> ({})'.format(payload_dict.items()))
    if payload_dict['sect1'] in ('Outlet', 'outlet', 'Outlets', 'outlets', 'Out', 'out', 'O', 'o') and (n_sect > 1):
        outlet_manager(payload_dict)
        info = relays.retrieve_info_states()
        print('O1: {}, O2: {}, O3: {}, O4: {}'.format(info[0], info[1], info[2], info[3]))

#--------------------------------MAIN CODE-------------------------------

ds, relays = var.ds, var.relays
client = MQTTClient(var.ADAFRUIT_IO['USERNAME'], var.ADAFRUIT_IO['KEY'])
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()

print('Number of DS18B20 sensors detected: {}'.format(var.num_ds))
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
   #sensor_values = (ds.temp(), bmp.pressure(), bmp.altitude('ft'), bh.light('lux'), pir.motion(t_last_motion))
   client.loop()
   if (time.time() - var.last) >= var.sample_rate:
       var.room_temp = ds.temp()
       #print('Publishing {0:.2f}F to RoomTemp feed.'.format(var.room_temp))
       client.publish(var.PUB_FEEDS['temp'], var.room_temp)
       var.last = time.time()

#------------------------------------------------------------------------
