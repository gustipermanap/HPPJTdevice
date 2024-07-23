import serial
import time

def parse_gga(line):
    parts = line.split(',')
    if parts[0] == "$GPGGA":
        latitude = parts[2]
        longitude = parts[4]
        return f"Latitude: {latitude}, Longitude: {longitude}"
    return None

ser = serial.Serial('/dev/serial0', 9600, timeout=1)

while True:
    data = ser.readline().decode('utf-8').strip()
    if data:
        location = parse_gga(data)
        if location:
            print(location)
    time.sleep(1)
