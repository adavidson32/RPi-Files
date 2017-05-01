import bmp280 as BMP280
from time import sleep

bmp = BMP280()

while 1:
    print('temp = {}'.format(bmp.temp()))
    print('pressure = {}'.format(bmp.pressure()))
    sleep(1)
