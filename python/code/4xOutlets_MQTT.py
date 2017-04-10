import os
import glob
import random
import sys
import time
import RPi.GPIO as GPIO
from Adafruit_IO import MQTTClient

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

O1P = 5
O2P = 6
O3P = 13
O4P = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(O1P, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(O2P, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(O3P, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(O4P, GPIO.OUT, initial=GPIO.HIGH)

ADAFRUIT_IO_KEY      = '11e4014862694ae6a474e89ece59c049'
ADAFRUIT_IO_USERNAME = 'adavidson93'

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
  f = open(device_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

def read_temp():
  lines = read_temp_raw()
  while lines[0].strip()[-3:] != 'YES':
    time.sleep(0.2)
    lines = read_temp_raw()
  equals_pos = lines[1].find('t=')
  if equals_pos != -1:
    temp_string = lines[1][equals_pos+2:]
    temp_c = float(temp_string) / 1000.0
    temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c, temp_f
                                                   
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    client.subscribe('IFTTT')

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload=='Outet1-ON':
      GPIO.output(O1P, GPIO.LOW)
      print('Outlet-1 Turned ON')
    elif payload=='Outlet1-OFF'
      GPIO.outlet(O1P, GPIO.HIGH)
      print('Outlet-1 Turned OFF')
    elif payload=='Outlet2-ON'
      GPIO.outlet(O2P, GPIO.LOW)
      print('Outlet-2 Turned ON')
    elif payload=='Outlet2-OFF'
      GPIO.outlet(O2P, GPIO.HIGH)
      print('Outlet-2 Turned OFF')
    elif payload=='Outlet3-ON'
      GPIO.outlet(O3P, GPIO.LOW)
      print('Outlet-3 Turned ON')
    elif payload=='Outlet3-OFF'
      GPIO.outlet(O3P, GPIO.HIGH)
      print('Outlet-3 Turned OFF')
    elif payload=='Outlet4-ON'
      GPIO.outlet(O4P, GPIO.LOW)
      print('Outlet-4 Turned ON')
    elif payload=='Outlet4-OFF'
      GPIO.outlet(O4P, GPIO.HIGH)
      print('Outlet-4 Turned OFF')
    elif payload=='Outlet1234-ON'
      GPIO.outlet(O1P, GPIO.LOW)
      GPIO.outlet(O2P, GPIO.LOW)
      GPIO.outlet(O3P, GPIO.LOW)
      GPIO.outlet(O4P, GPIO.LOW)
      print('All Outlets Turned ON')
    elif payload=='Outlet1234-OFF'
      GPIO.outlet(O1P, GPIO.HIGH)
      GPIO.outlet(O2P, GPIO.HIGH)
      GPIO.outlet(O3P, GPIO.HIGH)
      GPIO.outlet(O4P, GPIO.HIGH)
      print('All Outlets Turned OFF')

# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.  

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()
# Now send new values every 60 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
    RoomTemp = read_temp()
    print('Publishing {0} to IFTTT.'.format(RoomTemp))
    client.publish('IFTTT', RoomTemp)
    time.sleep(60)

# Another option is to pump the message loop yourself by periodically calling
# the client loop function.  Notice how the loop below changes to call loop
# continuously while still sending a new message every 10 seconds.  This is a
# good option if you don't want to or can't have a thread pumping the message
# loop in the background.
#last = 0
#print 'Publishing a new message every 10 seconds (press Ctrl-C to quit)...'
#while True:
#   # Explicitly pump the message loop.
#   client.loop()
#   # Send a new message every 10 seconds.
#   if (time.time() - last) >= 10.0:
#       value = random.randint(0, 100)
#       print 'Publishing {0} to DemoFeed.'.format(value)
#       client.publish('DemoFeed', value)
#       last = time.time()

# The last option is to just call loop_blocking.  This will run a message loop
# forever, so your program will not get past the loop_blocking call.  This is
# good for simple programs which only listen to events.  For more complex programs
# you probably need to have a background thread loop or explicit message loop like
# the two previous examples above.
#client.loop_blocking()
