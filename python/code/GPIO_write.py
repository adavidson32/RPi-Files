import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
if len(sys.argv) == 3:
  GPIO_pin = int(sys.argv[1])
  GPIO_function = sys.argv[2]
else:
  print("len(argv)!=3... Please manually enter GPIO_pin and GPIO_function")
  GPIO_pin = int(input("Which pin to control? : "))
  GPIO_function = input("Function to apply? : ")  

GPIO.setwarnings(False)
GPIO.setup(GPIO_pin, GPIO.OUT)

if (GPIO_function == "HIGH"):
  GPIO.output(GPIO_pin, GPIO.HIGH)
  print("GPIO#{0} set to HIGH...".format(GPIO_pin))
elif (GPIO_function == "LOW"):
  GPIO.output(GPIO_pin, GPIO.LOW)
  print("GPIO#{0} set to LOW...".format(GPIO_pin))
