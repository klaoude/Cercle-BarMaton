import RPi.GPIO as GPIO
import os
import time
import base64
import socket
import sys
import qrcode

DEBUG = 0

if sys.argv[1] == "-d":
    DEBUG = 1

URL_DNS = ""
URL_IP  = socket.gethostbyname(socket.gethostname())

BUTTON_PIN = 12

WWW = URL_DNS
PORT = 80

if URL_DNS == "":
    print "DNS disable, IP = {}".format(URL_IP)
    WWW = URL_IP

GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN)

while True:
    if DEBUG:
        input()
    else:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
    
    os.system("fswebcam --no-banner uploads/"+base64.b64encode(time.time())+".png")
    url = "http://" + WWW + "/upload"
    qr = qrcode.make(url)
    print qr
