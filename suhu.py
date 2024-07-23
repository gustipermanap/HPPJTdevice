import time
import board
import busio
from adafruit_mlx90614 import MLX90614  # Pastikan mengimpor MLX90614 dari adafruit_mlx90614

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create MLX90614 object.
sensor = MLX90614(i2c)

while True:
    print("Suhu Ambient: {:.2f} C".format(sensor.ambient_temperature))
    print("Suhu Objek: {:.2f} C".format(sensor.object_temperature))
    time.sleep(1)
