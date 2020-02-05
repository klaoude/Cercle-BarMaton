import os
import time
import base64
import socket
import sys
import qrcode
import pygame
from pygame.locals import *

DEBUG = 0
UPLOAD_DIR = "uploads/"
QR_DIR = UPLOAD_DIR + "qr/"

if len(sys.argv) > 1 and sys.argv[1] == "-d":
    DEBUG = 1
else:
    import RPi.GPIO as GPIO

URL_DNS = "localhost"
URL_IP  = socket.gethostbyname(socket.gethostname())

BUTTON_PIN = 12

WWW = URL_DNS
PORT = 80

if URL_DNS == "":
    print "DNS disable, IP = {}".format(URL_IP)
    WWW = URL_IP

if not DEBUG:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(BUTTON_PIN, GPIO.IN)

def get_image_and_QR():
    filename = base64.b64encode(str(time.time()))+".png"
    os.system("fswebcam --no-banner " + UPLOAD_DIR + filename)
    url = "http://" + WWW + "/" + UPLOAD_DIR + filename
    qr = qrcode.make(url)
    qr.save(QR_DIR + filename, "PNG")
    return filename

def show_images_on_screen(window):
    file = get_image_and_QR()
    img = pygame.image.load(UPLOAD_DIR + file)
    img_rect = img.get_rect()
    qr = pygame.image.load(QR_DIR + file)
    qr_rect = qr.get_rect()
    window.blit(img, img_rect)
    window.blit(qr, (400, 0))

pygame.init()
window = pygame.display.set_mode((800, 600))
exit = 0

while not exit:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit = 1
        if DEBUG and event.type == KEYDOWN:
            show_images_on_screen(window)
        if DEBUG and event.type == MOUSEBUTTONDOWN:
            print "pos = {}".format(event.pos)
    
    if not DEBUG:
        GPIO.wait_for_edge(BUTTON_PIN, GPIO.RISING)
        show_images_on_screen(window)

    pygame.display.flip()
    
