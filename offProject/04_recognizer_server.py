from http.server import HTTPServer, BaseHTTPRequestHandler

from urllib.parse import parse_qs

from io import BytesIO

import numpy as np

import cv2

import sys

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')

    def do_POST(self):
        print('POST RECIEVED')
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(205)
        self.end_headers()
        response = BytesIO()
        response.write(b'Tedt')
        parsed = parse_qs(body)
        shape = np.array(parsed[b'shape']).astype('int')
        data = np.array(parsed[b'data']).astype('float')
        data = data.reshape(shape)

        id, confidence = recognizer.predict(data)
        confidence = '{}'.format(confidence)
        response.write(bytes(confidence, 'utf-8'))

        self.wfile.write(response.getvalue())
print('Starting')

recognizer = cv2.face.LBPHFaceRecognizer_create()
print('Reading trainer.yml')
recognizer.read('trainer/trainer.yml')
print('trainer.yml was read')


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)

httpd.serve_forever()
