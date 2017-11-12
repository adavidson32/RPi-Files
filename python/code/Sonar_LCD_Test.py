import os, glob, time, sys, lcddriver
import RPi.GPIO as GPIO

LCD_BACKLIGHT = 0x08
LCD_NOBACKLIGHT = 0x00

sample_rate = 0.5
green_distance = 1
yellow_distance = 1
red_distance = 1

Green_Light, Yellow_Light, Red_Light, Relay4_Pin = 5, 6, 13, 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(Green_Light, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Yellow_Light, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Red_Light, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(Relay4_Pin, GPIO.OUT, initial=GPIO.HIGH)

def clear_lcd():
  lcd.lcd_display_string("                ", 1)
  lcd.lcd_display_string("                ", 2)
  
def lcd_print(distance, which_light)
  clear_lcd()

def which_color(distance):
  if distance <= red_distance:
    return "red"
  elif distance <= yellow_distance:
    return "yellow"
  elif distance <= green_distance:
    return "green"
  else:
    return "none"
    
def read_sonar():
  return distance
    
lcd = lcddriver.lcd()
clear_lcd()

while True:
  dist = read_sonar()
  lcd_print(dist, which_color(dist))
  time.sleep(sample_rate)
