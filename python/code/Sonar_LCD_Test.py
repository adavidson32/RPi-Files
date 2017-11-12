import os, glob, time, sys, lcddriver
import RPi.GPIO as GPIO

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

sample_rate = 0.5
room_temp = 10.0
green_distance = 4
yellow_distance = 1.5
red_distance = 0.5

Green_Light, Yellow_Light, Red_Light, Relay4_Pin = 5, 6, 13, 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(Green_Light, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Yellow_Light, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Red_Light, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Relay4_Pin, GPIO.OUT, initial=GPIO.HIGH)

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
  
def lcd_print(distance, which_light, temp):
  clear_lcd()
  str1 = "D={0:2.2f}m->{1}".format(distance, which_light)
  str2 = "Temp. = {0:2.2f} *F"
  lcd.lcd_display_string(str1, 1)
  lcd.lcd_display_string(str2, 2)

def which_color(distance):
  if distance <= red_distance:
    GPIO.output(Green_Light, GPIO.HIGH)
    GPIO.output(Yellow_Light, GPIO.HIGH)
    GPIO.output(Red_Light, GPIO.LOW)
    return "RED   "
  elif distance <= yellow_distance:
    GPIO.output(Green_Light, GPIO.HIGH)
    GPIO.output(Yellow_Light, GPIO.LOW)
    GPIO.output(Red_Light, GPIO.HIGH)
    return "YELLOW"
  elif distance <= green_distance:
    GPIO.output(Green_Light, GPIO.LOW)
    GPIO.output(Yellow_Light, GPIO.HIGH)
    GPIO.output(Red_Light, GPIO.HIGH)
    return "GREEN "
  else:
    GPIO.output(Green_Light, GPIO.HIGH)
    GPIO.output(Yellow_Light, GPIO.HIGH)
    GPIO.output(Red_Light, GPIO.HIGH)
    return "NONE  "
    
def read_sonar():
  return 4.319043
    
lcd = lcddriver.lcd()
clear_lcd()

while True:
  dist = read_sonar()
  which_light = which_color(dist)
  room_temp = read_temp()
  lcd_print(dist, which_light, room_temp)
  time.sleep(sample_rate)
