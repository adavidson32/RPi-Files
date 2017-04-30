#--------------------------single_relay.py------------------------------

# Use:
#    from single_relay.py import relay
#    device = relay(5)....
#    device.on()            -->  turns device ON
#    device.off()           -->  turns device off
#    device.flip()          -->  flips device state, returns new state
#    device.set(new_value)  -->  sets device to new_value
#    device.state()         -->  returns current state of device

#-----------------------INITIALIZE+SETUP DS18B20-------------------------

import RPi-GPIO as io

class relay:
    def __init__(self, pin):
        io.setmode(io.BCM)
        io.setwarnings(False)
        self.pin = pin
        io.setup(self.pin, io.OUT, initial=HIGH)
        self.state = 0

#-----------------------DEVICE FUNCTIONS---------------------------------

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

#-----------------------------------------------------------------------
