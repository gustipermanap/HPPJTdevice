from smbus2 import SMBus
from mlx90614 import MLX90614
import time 

bus = SMBus(1)
sensor = MLX90614(bus, address=0x5A)
while True:
	print ("suhu sekitar (ambient) :", sensor.get_amb_temp())
	print ("Suhu objek :", sensor.get_obj_temp())
	time.sleep(1)
bus.close()
