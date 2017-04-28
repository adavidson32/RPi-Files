# Usage:
#   ds = DS18B20('f')  <-- initialize ds18b20 1-wire bus to name 'ds' using fahrenheit units (
#   temp_1 = ds.temp(0)  <-- return temp value for sensor #0 (float)
#   all_temps = ds.temps()  <-- return all temp values on 1-wire bus (tuple of floats)
#   num_devices = ds.device_count()  <-- returns number of ds18b20 sensors detected (int)

import os, glob, time

class DS18B20:
   def __init__(self, units='c', decimal_places=2):
      if units == 'c':
        self.units = 1
      elif units == 'f':
        self.units = 0
      else:
        print("invalid entry for units. enter 'c' or 'f'.")
      # load required kernel modules
      os.system('modprobe w1-gpio')
      os.system('modprobe w1-therm')
      # Find file names for the sensor(s)
      base_dir = '/sys/bus/w1/devices/'
      device_folder = glob.glob(base_dir + '28*')
      self._num_devices = len(device_folder)
      self._device_file = list()
      self.dec_places = decimal_places
      i = 0
      while i < self._num_devices:
         self._device_file.append(device_folder[i] + '/w1_slave')
         i += 1

   def _read_temp(self,index):
      # Issue one read to one sensor
      # you should not call this directly
      f = open(self._device_file[index],'r')
      lines = f.readlines()
      f.close()
      return lines

   def temp(self, index=0):
      # call this to get the temperature in degrees C
      # detected by a sensor
      lines = self._read_temp(index)
      retries = 5
      while (lines[0].strip()[-3:] != 'YES') and (retries > 0):
         # read failed so try again
         time.sleep(0.1)
         #print('Read Failed', retries)
         lines = self._read_temp(index)
         retries -= 1
      if retries == 0:
         return 998
      equals_pos = lines[1].find('t=')
      if equals_pos != -1:
         temp = lines[1][equals_pos + 2:]
         temp_c = float(temp)/1000
         if units: 
            return round(temp_c, self.dec_places)
         elif not(units):
            temp_f = ((temp_c * 1.8) + 32.0)
            return round(temp_f, self.dec_places)
      else:
         # error
         return 999

   def temps(self):
      temps = ('',)
      for i in range(device_count):
         temps += (round(temp(i), self.dec_places),)
      return temps[1:]

   def device_count(self):
      # call this to see how many sensors have been detected
      return self._num_devices
