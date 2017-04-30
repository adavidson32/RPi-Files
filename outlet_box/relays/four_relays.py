#--------------------------four_relays.py-------------------------------

# To use four_relays.py:
#     from four_relays import four_relays
#     outlet_pins = [4, 5, 6, 9]
#     outlet_names = ('bed light', 'futon light', 'desk light', 'iPhone charger')
#     ex. relays = four_relays(outlet_pins, outlet_names)
#     relays.on('all'), relays.on(1), relays.on([2,3,4]), relays.on('outlets-134'), relays.on(('bed light', 'futon light'))

#-----------------------INITIALIZE+SETUP DS18B20-------------------------

from single_relay import relay

class four_relays:
  def __init__(self, pins, names):
    self.O1 = relay(pins[0])
    self.O2 = relay(pins[1])
    self.O3 = relay(pins[2])
    self.O4 = relay(pins[3])
    self.O1_name = names[0]
    self.O2_name = names[1]
    self.O3_name = names[2]
    self.O4_name = names[3]

#---------------------------ON FUNCTIONS---------------------------------

  def on(self, outlets):

    if (type(outlets) == type(('',))):
      for name in outlets:
        if name == self.O1_name:
          self.O1.on()
        elif name == self.O2_name:
          self.O2.on()
        elif name == self.O3_name:
          self.O3.on()
        elif name == self.O4_name:
          self.O4.on()
    elif (type(outlets) == type([1,2,3])):
      for num in outlets:
        if num == 1:
          self.O1.on()
        elif num == 2:
          self.O2.on()
        elif num == 3:
          self.O3.on()
        elif num == 4:
          self.O4.on()
    elif (type(outlets) == type(4)):
      if outlets == 1:
        self.O1.on()
      elif outlets == 2:
        self.O2.on()
      elif outlets == 3:
        self.O3.on()
      elif outlets == 4:
        self.O4.on()
      elif outlets == 1234:
        self.on('all')
    elif (type(outlets) == type('str')):
      if outlets == self.O1_name:
        self.O1.on()
      elif outlets == self.O2_name:
        self.O2.on()
      elif outlets == self.O3_name:
        self.O3.on()
      elif outlets == self.O4_name:
        self.O4.on()
      elif outlets == 'all':
        self.O1.on()
        self.O2.on()
        self.O3.on()
        self.O4.on()
      elif outlets[0:7] == 'outlets-':
        num = len(outlets) - 8
        for i in range(num):
          if int(outlets[i+8]) == 1:
            self.O1.on()
          elif int(outlets[i+8]) == 2:
            self.O2.on()
          elif int(outlets[i+8]) == 3:
            self.O3.on()
          elif int(outlets[i+8]) == 4:
            self.O4.on()

#---------------------------OFF FUNCTIONS--------------------------------

  def off(self, outlets):
    if (type(outlets) == type(('',))):
      for name in outlets:
        if name == self.O1_name:
          self.O1.off()
        elif name == self.O2_name:
          self.O2.off()
        elif name == self.O3_name:
          self.O3.off()
        elif name == self.O4_name:
          self.O4.off()
    elif (type(outlets) == type([1,2,3])):
      for num in outlets:
        if num == 1:
          self.O1.off()
        elif num == 2:
          self.O2.off()
        elif num == 3:
          self.O3.off()
        elif num == 4:
          self.O4.off()
    elif (type(outlets) == type(4)):
      if outlets == 1:
        self.O1.off()
      elif outlets == 2:
        self.O2.off()
      elif outlets == 3:
        self.O3.off()
      elif outlets == 4:
        self.O4.off()
      elif outlets == 1234:
        self.on('all')
    elif (type(outlets) == type('str')):
      if outlets == self.O1_name:
        self.O1.off()
      elif outlets == self.O2_name:
        self.O2.off()
      elif outlets == self.O3_name:
        self.O3.off()
      elif outlets == self.O4_name:
        self.O4.off()
      elif outlets == 'all':
        self.O1.off()
        self.O2.off()
        self.O3.off()
        self.O4.off()
      elif outlets[0:7] == 'outlets-':
        num = len(outlets) - 8
        for i in range(num):
          if int(outlets[i+8]) == 1:
            self.O1.off()
          elif int(outlets[i+8]) == 2:
            self.O2.off()
          elif int(outlets[i+8]) == 3:
            self.O3.off()
          elif int(outlets[i+8]) == 4:
            self.O4.off()
