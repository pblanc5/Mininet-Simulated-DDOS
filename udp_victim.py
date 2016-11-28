import socket

#============================================================
# Module: victim.py
# Author: Patrick Blanchard
# Purpose: Creates victim udp server.
# Date: November 8, 2016
#=============================================================

PORT = 5000
HOST = ""

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))

while True:
    msg, add = s.recvfrom(1024)
