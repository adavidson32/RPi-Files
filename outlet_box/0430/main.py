#-------------------------------main.py----------------------------------

import time, sys
from variables import variables
sys.path.append('/home/pi/git/RPi-Files/outlet_box/relays')
sys.path.append('/home/pi/git/RPi-Files/outlet_box/sensors')
sys.path.append('/home/pi/git/RPi-Files/outlet_box/0430')
from Adafruit_IO import MQTTClient
from four_relays import four_relays
from type_test import type_test
from ds18b20 import DS18B20



#-----------------------ADAFRUIT-IO CALLBACKS----------------------------

def payload_seperator(payload, seperator=','):
    n_sect = payload.count(seperator) + 1
    sections = [x.strip() for x in payload.split(seperator)]
    sect_range = range(len(sections))
    sect_names = ['sect{}'.format(i+1) for i in sect_range]
    sect_values = [sections[i] for i in sect_range]
    payload_dict = dict(((sect_names[i], sect_values[i]) for i in sect_range))
    payload_dict['n_sect'] = n_sect
    for i in sect_range:
        print("name->('{}'), value->('{}'), payload_dict[name]->('{}')". format(sect_names[i], sect_values[i], payload_dict[sect_names[i]]))
    if n_sect > 4:
        print('n_sect is out of range (currenly: {}). Must be between 1,4'.format(n_sect))
    return payload_dict

def outlet_manager(payload_dict):
    addr = payload_dict['sect2']
    if addr in ('ALL', 'All', 'all', '*', 'a', ':', '1234', 1234):
        outlet_addr = 'all'
    elif addr in (1, 2, 3, 4, '1', '2', '3', '4'):
        outlet_addr = int(addr)
    elif addr in var.outlet_names:
        outlet_addr = addr
    else:
        outlet_addr = 'all'
        print('outlet address outside of range (1/2/3/4/*), using default-->(all)')
    if (payload_dict['n_sect'] in [3,4]):
        func = payload_dict['sect3']
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
    if payload_dict['sect1'] in ('Outlet', 'outlet', 'Outlets', 'outlets', 'Out', 'out', 'O', 'o') and (n_sect > 1):
        outlet_manager(payload_dict)
        info = relays.retrieve_info_states()
        print('O1: {}, O2: {}, O3: {}, O4: {}'.format(info[0], info[1], info[2], info[3]))



#--------------------------------MAIN CODE-------------------------------

var = variables()
ADAFRUIT_IO, PUB_FEEDS, SUB_FEEDS = var.ADAFRUIT_IO, var.PUB_FEEDS, var.SUB_FEEDS

relays = four_relays(var.outlet_pins, var.outlet_names, var.outlet_types)
ds = DS18B20('f', 2)
num_ds = var.num_ds = ds.num_ds()

client = MQTTClient(ADAFRUIT_IO['USERNAME'], ADAFRUIT_IO['KEY'])
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()

print('Number of DS18B20 sensors detected: {}'.format(var.num_ds))
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
try:
    while True:
       #sensor_values = (ds.temp(), bmp.pressure(), bmp.altitude('ft'), bh.light('lux'), pir.motion(t_last_motion))
       client.loop()
       if (time.time() - var.last) >= var.sample_rate:
           var.room_temp = ds.temp()
           #print('Publishing {0:.2f}F to RoomTemp feed.'.format(var.room_temp))
           client.publish(PUB_FEEDS['temp'], var.room_temp)
           var.last = time.time()
except KeyboardInterrupt:
    relays.cleanup()


#------------------------------------------------------------------------
