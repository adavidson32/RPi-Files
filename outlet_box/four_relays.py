# To use four_relays.py:
#     from four_relays import four_relays
#     outlet_pins = [4, 5, 6, 9]
#     outlet_names = ('bed light', 'futon light', 'desk light', 'iPhone charger')
#     ex. relays = four_relays(outlet_pins, outlet_names)
#     relays.on('all'), relays.on(1), relays.on([2,3,4]), relays.on('outlets-134'), relays.on(('bed light', 'futon light'))

from single_relay import relay

class four_relays:
  def __init__(self, pins, names):
    self.out1 = relay(pins[0])
    self.out2 = relay(pins[1])
    self.out3 = relay(pins[2])
    self.out4 = relay(pins[3])
    self.out1_name = names[0]
    self.out2_name = names[1]
    self.out3_name = names[2]
    self.out4_name = names[3]
 
  def on(self, outlets):
    if (type(outlets) == type(('',))):
      for name in outlets:
        if name == self.out1_name:
          self.out1.on()
        elif name == self.out2_name:
          self.out2.on()
        elif name == self.out3_name:
          self.out3.on()
        elif name == self.out4_name:
          self.out4.on()
    elif (type(outlets) == type([1,2,3])):
      for num in outlets:
        if num == 1:
          self.out1.on()
        elif num == 2:
          self.out2.on()
        elif num == 3:
          self.out3.on()
        elif num == 4:
          self.out4.on()
    elif (type(outlets) == type(4)):
      if outlets == 1:
        self.out1.on()
      elif outlets == 2:
        self.out2.on()
      elif outlets == 3:
        self.out3.on()
      elif outlets == 4:
        self.out4.on()
      elif outlets == 1234:
        self.on('all')
    elif (type(outlets) == type('str')):
      if outlets == self.out1_name:
        self.out1.on()
      elif outlets == self.out2_name:
        self.out2.on()
      elif outlets == self.out3_name:
        self.out3.on()
      elif outlets == self.out4_name:
        self.out4.on()
      elif outlets == 'all':
        self.out1.on()
        self.out2.on()
        self.out3.on()
        self.out4.on()
      elif outlets[0:7] == 'outlets-':
        num = len(outlets) - 8
        for i in range(num):
          if int(outlets[i+8]) == 1:
            self.out1.on()
          elif int(outlets[i+8]) == 2:
            self.out2.on()
          elif int(outlets[i+8]) == 3:
            self.out3.on()
          elif int(outlets[i+8]) == 4:
            self.out4.on() 
            
            
  def off(self, outlets):
    if (type(outlets) == type(('',))):
      for name in outlets:
        if name == self.out1_name:
          self.out1.off()
        elif name == self.out2_name:
          self.out2.off()
        elif name == self.out3_name:
          self.out3.off()
        elif name == self.out4_name:
          self.out4.off()
    elif (type(outlets) == type([1,2,3])):
      for num in outlets:
        if num == 1:
          self.out1.off()
        elif num == 2:
          self.out2.off()
        elif num == 3:
          self.out3.off()
        elif num == 4:
          self.out4.off()
    elif (type(outlets) == type(4)):
      if outlets == 1:
        self.out1.off()
      elif outlets == 2:
        self.out2.off()
      elif outlets == 3:
        self.out3.off()
      elif outlets == 4:
        self.out4.off()
      elif outlets == 1234:
        self.on('all')
    elif (type(outlets) == type('str')):
      if outlets == self.out1_name:
        self.out1.off()
      elif outlets == self.out2_name:
        self.out2.off()
      elif outlets == self.out3_name:
        self.out3.off()
      elif outlets == self.out4_name:
        self.out4.off()
      elif outlets == 'all':
        self.out1.off()
        self.out2.off()
        self.out3.off()
        self.out4.off()
      elif outlets[0:7] == 'outlets-':
        num = len(outlets) - 8
        for i in range(num):
          if int(outlets[i+8]) == 1:
            self.out1.off()
          elif int(outlets[i+8]) == 2:
            self.out2.off()
          elif int(outlets[i+8]) == 3:
            self.out3.off()
          elif int(outlets[i+8]) == 4:
            self.out4.off()
