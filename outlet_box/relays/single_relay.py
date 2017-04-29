# single_relay.py
# Use:
#    from single_relay.py import relay
#    O1 = relay(5)
#    O2 = relay(6).....
#    O1.on()
#    O1_current_state = O1.state()
#    O2.set(1)
#    new = O1.flip()  <-- flips O1 and returns new set value

import RPi-GPIO as io

class relay:
    def __init__(self, pin):
	io.setmode(io.BCM)
	io.setwarnings(False)
	self.pin = pin
	io.setup(self.pin, io.OUT, initial=HIGH)
	self.state = 0

    def on(self):
        self.state = 1
	io.output(self.pin, io.LOW)

    def off(self):
        self.state = 0
	io.output(self.pin, io.HIGH)
	
    def flip(self):
	if self.state:
	    self.off()
	elif not(self.state):
	    self.on()
	return self.state
	
    def set(self, set_value):
	if set_value:
		self.on()
	elif not(set_value):
		self.off()

    def state(self):
        return self.state
