import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
if not(len(sys.argv) == 3):
  print("len(argv)!=3... Please manually enter GPIO_pin and GPIO_function")
  GPIO_pin = int(input("Which pin to control? : "))
  GPIO_function = input("Function to apply? : ")
else:
  GPIO_pin = int(sys.argv[1])
  GPIO_function = sys.argv[2]

print("GPIO_pin : ", GPIO_pin)
print("GPIO_function : ", GPIO_function)

GPIO.setup(GPIO_pin, GPIO.OUT)

if (GPIO_function == "HIGH"):
  GPIO.output(GPIO_pin, GPIO.HIGH)
elif (GPIO_function == "LOW"):
  GPIO.output(GPIO_pin, GPIO.LOW)
