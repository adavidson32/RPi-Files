import RPi-GPIO as io
from time import sleep, time

class relays:
    def __init__(self, pin, active_low=True):
	io.setmode(io.BCM)
	io.setwarnings(
	self.pin = pin
	self.active_low = active_low
	io.setup(self.pin, io.OUT)
	if active_low:
	    io.output(self.pin, io.HIGH)
	elif not(active_low):
	    io.output(self.pin, io.LOW)

    def on(self):
	if self.active_low:
	    io.output(self.pin, io.LOW)
	else:
	    io.output(self.pin, io.HIGH)


