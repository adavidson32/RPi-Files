import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)
GPIO.output(18, True)
GPIO.output(23, True)
GPIO.output(24, True)
GPIO.output(25, True)

while True:
  GPIO.output(18, False)
  time.sleep(0.5)
  GPIO.output(18, True)
  GPIO.output(23, False)
  time.sleep(0.5)
  GPIO.output(23, True)
  GPIO.output(24, False)
  time.sleep(0.5)
  GPIO.output(24, True)
  GPIO.output(25, False)
  time.sleep(0.5)
  GPIO.output(25, True)
GPIO.cleanup()
