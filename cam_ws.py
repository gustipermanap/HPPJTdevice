from websocket import create_connection
from threading import Condition
import picamera
import sys
import io

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


IDENTIFIER = sys.argv[1]

ws = create_connection("ws://192.168.26.239:8000/ws/camera/%s/send/" % IDENTIFIER)

with picamera.PiCamera(resolution="300x300", framerate=24) as camera:
  output = StreamingOutput()
  camera.vflip = True
  camera.hflip = True
  camera.start_recording(output, format='mjpeg')
  while True:
    with output.condition:
      output.condition.wait()
      frame = output.frame
    ws.send_binary(frame)
