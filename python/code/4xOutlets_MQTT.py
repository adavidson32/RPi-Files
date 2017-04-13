import os, glob, time, sys, lcddriver
from Adafruit_IO import MQTTClient
import RPi.GPIO as GPIO

O1P, O2P, O3P, O4P = 5, 6, 13, 19
LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00
ADAFRUIT_IO_KEY      = '11e4014862694ae6a474e89ece59c049'
ADAFRUIT_IO_USERNAME = 'adavidson93'
SUB_FEED = 'IFTTT'
PUB_FEED = 'RoomTemp'
sample_rate = 10.0
room_temp = 10.0

GPIO.setmode(GPIO.BCM)
GPIO.setup(O1P, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(O2P, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(O3P, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(O4P, GPIO.OUT, initial=GPIO.HIGH)

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
def clear_lcd():
    lcd.lcd_display_string("                ", 1)
    lcd.lcd_display_string("                ", 2)
def connected(client):
    print("Connected to Adafruit IO!  Listening for {0} changes".format(SUB_FEED))
    clear_lcd()
    lcd.lcd_display_string("Conn adafruit.io", 1)
    lcd.lcd_display_string("usr: {}".format(ADAFRUIT_IO_USERNAME), 2)
    client.subscribe(SUB_FEED)
def disconnected(client):
    print('Disconnected from Adafruit IO!')
    clear_lcd()
    sys.exit(1)
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload == "Outet1-ON":
      GPIO.output(O1P, GPIO.LOW)
      print('Outlet-1 Turned ON')
    elif payload == "Outlet1-OFF":
      GPIO.output(O1P, GPIO.HIGH)
      print('Outlet-1 Turned OFF')
    elif payload == "Outlet2-ON":
      GPIO.output(O2P, GPIO.LOW)
      print('Outlet-2 Turned ON')
    elif payload == "Outlet2-OFF":
      GPIO.output(O2P, GPIO.HIGH)
      print('Outlet-2 Turned OFF')
    elif payload == "Outlet3-ON":
      GPIO.output(O3P, GPIO.LOW)
      print('Outlet-3 Turned ON')
    elif payload == "Outlet3-OFF":
      GPIO.output(O3P, GPIO.HIGH)
      print('Outlet-3 Turned OFF')
    elif payload == "Outlet4-ON":
      GPIO.output(O4P, GPIO.LOW)
      print('Outlet-4 Turned ON')
    elif payload == "Outlet4-OFF":
      GPIO.output(O4P, GPIO.HIGH)
      print('Outlet-4 Turned OFF')
    elif payload == "Outlet1234-ON":
      GPIO.output(O1P, GPIO.LOW)
      GPIO.output(O2P, GPIO.LOW)
      GPIO.output(O3P, GPIO.LOW)
      GPIO.output(O4P, GPIO.LOW)
      print('All Outlets Turned ON')
    elif payload == "Outlet1234-OFF":
      GPIO.output(O1P, GPIO.HIGH)
      GPIO.output(O2P, GPIO.HIGH)
      GPIO.output(O3P, GPIO.HIGH)
      GPIO.output(O4P, GPIO.HIGH)
      print('All Outlets Turned OFF')
    elif payload == "Backlight-OFF":
      lcd.lcd_device.write_cmd(data | LCD_NOBACKLIGHT)
    elif payload == "Backlight-ON":
      lcd.lcd_device.write_cmd(data | LCD_BACKLIGHT)
    if len(payload) > 14:
        payload = payload[0:14]
    clear_lcd()
    len_feed_name = len(feed_id)
    extra_needed = (16 - len_feed_name - 3)
    spacer = ''
    for i in range(0,extra_needed):
        spacer += ' '
    lcd.lcd_display_string("F:{0} {1}{2:.1f}".format(feed_id, spacer, coffee_temp), 1)
    lcd.lcd_display_string("M:{}".format(payload), 2)

lcd = lcddriver.lcd()
clear_lcd()

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.connect()

last = 0
print('Publishing a new message every 30 seconds (press Ctrl-C to quit)...')
while True:
   client.loop()
   if (time.time() - last) >= sample_rate:
       coffee_temp = read_temp()
       print('Publishing {0:.2f}F to RoomTemp feed.'.format(coffee_temp))
       client.publish(PUB_FEED, coffee_temp)
       last = time.time()
