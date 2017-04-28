import RPi-GPIO as io
from time import sleep, time

class relays:
    def __init__(self, pin):
	io.setmode(io.BCM)
	io.setwarnings(False)
	self.pin = pin
	io.setup(self.pin, io.OUT, initial=HIGH)

    def on(self):
	io.output(self.pin, io.LOW)
		
    def off(self):
	io.output(self.pin, io.HIGH)
