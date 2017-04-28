import time, sys
from Adafruit_IO import MQTTClient
from four_relays import four_relays
from ds18b20 import DS18B20
from bmp280 import BMP280

# Outlets contains dictionairies for each Outlet.
# last = currently set, new = new value to set
# ex. Outlet-1 has pin 19, and is currently off
Outlets = {'O1': {'pin': 19, 'name': 'futon lights', 'last': 0, 'new': -1}, 
           'O2': {'pin': 5, 'name': 'iPhone charger', 'last': 0, 'new': -1}, 
           'O3': {'pin': 6, 'name': 'bed light', 'last': 0, 'new': -1}, 
           'O4': {'pin': 13, 'name': 'desk light', 'last': 0, 'new': -1}}

ds = DS18B20()
bmp = BMP280()
outlet_pins = (Outlets['O1']['pin'], Outlets['O2']['pin'], Outlets['O3']['pin'], Outlets['O4']['pin'])
outlet_names = (Outlets['O1']['name'], Outlets['O2']['name'], Outlets['O3']['name'], Outlets['O4']['name'])
relays = four_relays(outlet_pins, outlet_names)

# ADAFRUIT_IO dict with keys KEY and USERNAME
ADAFRUIT_IO = {'KEY': '11e4014862694ae6a474e89ece59c049', 'USERNAME': 'adavidson93'}
SUB_FEED = 'IFTTT'
PUB_FEED = 'RoomTemp'
sample_rate = 10.0 #How often to send temperature value
room_temp = 10.0 #Initial value (could be anything....)

def connected(client):
    print("Connected to Adafruit IO!  Listening for {0} changes".format(SUB_FEED))
    client.subscribe(SUB_FEED)
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload == "Outlet1-ON":
        Outlets['O1']['new'] = 1
    elif payload == "Outlet1-OFF":
        Outlets['O1']['new'] = 0
    elif payload == "Outlet1":
        Outlets['O1']['new'] = not(Outlets['O1']['last'])
    elif payload == "Outlet2-ON":
        Outlets['O2']['new'] = 1
    elif payload == "Outlet2-OFF":
        Outlets['O2']['new'] = 0
    elif payload == "Outlet2":
        Outlets['O2']['new'] = not(Outlets['O2']['last'])
    elif payload == "Outlet3-ON":
        Outlets['O3']['new'] = 1
    elif payload == "Outlet3-OFF":
        Outlets['O3']['new'] = 0
    elif payload == "Outlet3":
        Outlets['O3']['new'] = not(Outlets['O3']['last'])
    elif payload == "Outlet4-ON":
        Outlets['O4']['new'] = 1
    elif payload == "Outlet4-OFF":
        Outlets['O4']['new'] = 0
    elif payload == "Outlet4":
        Outlets['O4']['new'] = not(Outlets['O4']['last'])
    elif payload == "Outlet1234-ON":
        for i in Outlets:
            Outlets[i]['new'] = 1
    elif payload == "Outlet1234-OFF":
        for i in Outlets:
            Outlets[i]['new'] = 0
    elif payload == "Outlet1234":
        for i in Outlets:  
            Outlets[i]['new'] = not(Outlets[i]['last'])
    for x in Outlets:
        if not(Outlets[x]['new'] == -1):
            if Outlets[x]['new'] == 1:
                io.output(Outlets[x]['pin'], io.LOW)
            else:
                io.output(Outlets[x]['pin'], io.HIGH)                 
            Outlets[x]['last'] = Outlets[x]['new']
            Outlets[x]['new'] = -1
    print('O1: {}, O2: {}, O3: {}, O4: {}'.format(Outlets['O1']['last'], Outlets['O2']['last'], Outlets['O3']['last'], Outlets['O4']['last']))
    
client = MQTTClient(ADAFRUIT_IO['USERNAME'], ADAFRUIT_IO['KEY'])
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()

last = 0
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
   sensor_values = (ds.temp('f'), bmp.pressure('pa'), bmp.altitude('ft'), bh.light('lux'), pir.motion(t_last_motion))
   client.loop()
   if (time.time() - last) >= sample_rate:
       coffee_temp = read_temp()
       print('Publishing {0:.2f}F to RoomTemp feed.'.format(coffee_temp))
       client.publish(PUB_FEED, coffee_temp)
       last = time.time()
