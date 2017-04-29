import RPi-GPIO as io

class relays:
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

    def state(self):
        return self.state
