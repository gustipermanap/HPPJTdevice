import serial
import time
import pynmea2

while True:
  port="/dev/ttyAMA0"
  s = serial.Serial(port, baudrate=9600, timeout=0.5)
  o = pynmea2.NMEAStreamReader()
  d = s.readline()
  if d[0:6] == b"$GNRMC":
    nm = pynmea2.parse(d.decode('utf-8'))
    print("New Msg", nm)
    lat = nm.latitude
    lon = nm.longitude
    print(f"Lat: {lat}, Lon: {lon}")
