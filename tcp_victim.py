import socket

#============================================================
# Module: tcp_victim.py
# Author: Patrick Blanchard
# Purpose: Creates victim tcp server.
# Date: November 8, 2016
#=============================================================

PORT = 5000
HOST = ""

def defend():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        s.listen(1000)
        while True:
            conn, addr = s.accept()
            mesg = conn.recv(1024)
    except:
        print "Server Disconnected"
        pass

while True:
    defend()
