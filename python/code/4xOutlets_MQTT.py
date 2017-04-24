import os, glob, time, sys, lcddriver
from Adafruit_IO import MQTTClient
import RPi.GPIO as io

Outlets = {'O1': {'pin': 19, 'last': 0, 'new': -1}, 
           'O2': {'pin': 13, 'last': 0, 'new': -1}, 
           'O3': {'pin': 6, 'last': 0, 'new': -1}, 
           'O4': {'pin': 5, 'last': 0, 'new': -1}}
ADAFRUIT_IO = {'KEY': '11e4014862694ae6a474e89ece59c049', 'USERNAME': 'adavidson93'}
SUB_FEED = 'IFTTT'
PUB_FEED = 'RoomTemp'
sample_rate = 10.0 #How often to send temperature value
room_temp = 10.0 #Initial value (could be anything....)

io.setmode(io.BCM)
io.setup(Outlets['O1']['pin'], io.OUT, initial=io.HIGH)
io.setup(Outlets['O2']['pin'], io.OUT, initial=io.HIGH)
io.setup(Outlets['O3']['pin'], io.OUT, initial=io.HIGH)
io.setup(Outlets['O4']['pin'], io.OUT, initial=io.HIGH)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
device_folder = glob.glob('/sys/bus/w1/devices/28*')
device_file = device_folder[0] + '/w1_slave'
def read_temp_raw():
    f_1 = open(device_file, 'r')
    lines_1 = f_1.readlines()
    f_1.close()
    return lines_1
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    temp = float(lines[1][equals_pos+2:])/1000
    temp_f = (temp*1.8 + 32.0)
    return temp_f

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
        Outlets['01']['new'] = not(Outlets['01']['last'])
    elif payload == "Outlet2-ON":
        Outlets['O2']['new'] = 1
    elif payload == "Outlet2-OFF":
        Outlets['O2']['new'] = 0
    elif payload == "Outlet2":
        Outlets['02']['new'] = not(Outlets['02']['last'])
    elif payload == "Outlet3-ON":
        Outlets['O3']['new'] = 1
    elif payload == "Outlet3-OFF":
        Outlets['O3']['new'] = 0
    elif payload == "Outlet3":
        Outlets['03']['new'] = not(Outlets['03']['last'])
    elif payload == "Outlet4-ON":
        Outlets['O4']['new'] = 1
    elif payload == "Outlet4-OFF":
        Outlets['O4']['new'] = 0
    elif payload == "Outlet4":
        Outlets['04']['new'] = not(Outlets['04']['last'])
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
        if not(Outlets[x]['new'] == Outlets[x]['last']):
               io.output(Outlets[x]['pin'], Outlets[x]['new'])
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
   client.loop()
   if (time.time() - last) >= sample_rate:
       coffee_temp = read_temp()
       print('Publishing {0:.2f}F to RoomTemp feed.'.format(coffee_temp))
       client.publish(PUB_FEED, coffee_temp)
       last = time.time()
