import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

PAGE="""\
<html>
<head>
<title>HK - Hepi</title>
</head>
<body>
<center><img src="stream.mjpg" width="720" height="720"></center>
</body>
</html>
"""

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

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.send_header
                    self.wfile.write(b'--FRAME\r\n')
                    # self.send_header('Content-Type', 'image/jpeg')
                    # self.send_header('Content-Length', len(frame))
                    # self.end_headers()
                    self.wfile.write(bytes("Content-Type: image/jpeg\r\n", 'utf-8'))
                    self.wfile.write(bytes(f"Content-Length: {len(frame)}\r\n\r\n", 'utf-8'))
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='100x100', framerate=20) as camera:
    output = StreamingOutput()
    camera.resolution = (720, 720)  # Atur resolusi sesuai kebutuhan
    camera.iso = 100  # Atur ISO sesuai pencahayaan
    camera.exposure_mode = 'auto'  # Atur mode eksposur
    camera.vflip = True
    camera.hflip = True
    camera.color_effects = (128, 128)
    camera.start_recording(output, format='mjpeg')
    camera.color_effects = None
    try:
    #alamat
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()
