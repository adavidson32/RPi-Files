from single_relay import relay

# To use four_relays.py:
# from four_relays import four_relays
# ex. relays = four_relays(4, 5, 6, 9, ('bed light', 'futon light', 'desk light', 'iPhone charger')
#   


class four_relays:
  def __init__(self, O1P, O2P, O3P, O4P, names):
    self.out1 = relay(O1P)
    self.out2 = relay(O2P)
    self.out3 = relay(O3P)
    self.out4 = relay(O4P)
    self.out1_name = names[0]
    self.out2_name = names[1]
    self.out3_name = names[2]
    self.out4_name = names[3]
  
  def all_on(self):
    self.out1.on()
    self.out2.on()
    self.out3.on()
    self.out4.on()
    
  def all_off(self):
    self.out1.off()
    self.out2.off()
    self.out3.off()
    self.out4.off()
    
  def 1_on(self):
    self.out1.on()
    
  def 1_off(self):
    self.out1.off()
  
  def 2_on(self):
    self.out2.on()
  
  def 2_off(self):
    self.out2.off()
  
  def 3_on(self):
    self.out3.on()
  
  def 3_off(self):
    self.out3.off()
  
  def 4_on(self):
    self.out4.on()
  
  def 4_off(self):
    self.out4.off()
    
  def on(name):
    if name == self.out1_name:
      self.out1.on()
    elif name == self.out2_name:
      self.out2.on()
    elif name == self.out3_name:
      self.out3.on()
    elif name == self.out4_name:
      self.out4.on()
      
  def off(name):
    if name == self.out1_name:
      self.out1.off()
    elif name == self.out2_name:
      self.out2.off()
    elif name == self.out3_name:
      self.out3.off()
    elif name == self.out4_name:
      self.out4.off()
