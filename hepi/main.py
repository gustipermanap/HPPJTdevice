from smbus2 import SMBus
from mlx90614 import MLX90614
from websocket import create_connection
from gpiozero import Button
import RPi.GPIO as GPIO
from threading import Condition
import picamera
import io
import sys
import time
import json
import threading

IDENTIFIER = sys.argv[1]

GPIO.setmode(GPIO.BCM)

def safe_json_dumps(obj):
  return json.dumps(obj, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o), indent=4)

bus = SMBus(1)
temp_sensor = MLX90614(bus, address=0x5a)
help_button = Button(24)


ws = create_connection(f"ws://203.194.112.131/ws/helmet/{IDENTIFIER}/")
c_ws = create_connection(f"ws://203.194.112.131/ws/camera/{IDENTIFIER}/send/")

class StreamingOutput(object):
  def __init__(self):
    self.frame = None
    self.buffer = io.BytesIO()
    self.condition = Condition()

  def write(self, buf):
    if buf.startswith(b'\xff\xd8'):
      self.buffer.truncate()
      with self.condition:
        self.frame = self.buffer.getvalue()
        self.condition.notify_all()
      self.buffer.seek(0)
    return self.buffer.write(buf)

def cam_update():
  with picamera.PiCamera(resolution="100x100", framerate=20) as camera:
    output = StreamingOutput()
    camera.vflip = True
    camera.hflip = True
    camera.start_recording(output, format='mjpeg')
    while True:
      with output.condition:
        output.condition.wait()
        frame = output.frame
      c_ws.send_binary(frame)

def data_update():
  while True:
    data = {
      "type": "helmet_send_data",
      "temperature": temp_sensor.get_amb_temp(),
      "position": {
        "lat": -6.24531,
        "lon": 106.87318
      }
    }
    ws.send(safe_json_dumps(data))
    time.sleep(5)

def help_listener():
  while True:
    if help_button.is_pressed:
      data = {
        "type": "helmet_send_notification",
        "kind": "HELP"
      }
      ws.send(safe_json_dumps(data))
      time.sleep(1)

VIB_PIN = 22
def fall_callback(e):
  if GPIO.input(e):
    data = {
      "type": "helmet_send_notification",
      "kind": "FALL"
    }
    ws.send(safe_json_dumps(data))
    time.sleep(1)

GPIO.setup(VIB_PIN, GPIO.IN)
GPIO.add_event_detect(VIB_PIN, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(VIB_PIN, fall_callback)

t_du = threading.Thread(target=data_update)
t_du.daemon=True
t_du.start()

t_hl = threading.Thread(target=help_listener)
t_hl.daemon=True
t_hl.start()

t_cu = threading.Thread(target=cam_update)
t_cu.daemon=True
t_cu.start()

while True:
  pass
