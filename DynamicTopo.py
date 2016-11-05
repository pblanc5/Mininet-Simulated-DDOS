#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.nodelib import LinuxBridge
from mininet.node import OVSBridge

from optparse import OptionParser
import math

#============================================================
# Module: DynamicTopo.py
# Author: Patrick Blanchard
# Purpose: Creates a custom network based off a tree topology.
# Date: November 5, 2016
#=============================================================


class DynamicTopo( Topo ):
    "Simple topology example."
    hostList = []
    switchList = []


    def __init__( self, numHost, numLink, bandwidth ):
        "Create custom topo."
        Topo.__init__( self )

        L3 = int(math.ceil(float(numHost)/numLink))
        L2 = int(math.ceil(float(numLink)/L3))
        L1 = 1

        #Add Hosts
        for i in range(0, numHost):
            self.hostList.append(self.addHost('h%d' % (i+1)))
        #Add Switches
        for i in range(0, L2+L3+L1):
            self.switchList.append(self.addSwitch('s%d' % (i+1)))

        #Set links
        for i in range(0, L2):
            print "%s -> %s" % (self.switchList[0], self.switchList[L1+i])
            self.addLink(self.switchList[0], self.switchList[L1+i])

        for i in range(0, L2):
            for j in range(0, L3):
                print "\t%s -> %s" % (self.switchList[L1+i], self.switchList[L2+j+1])
                self.addLink(self.switchList[L1+i], self.switchList[L2+j+1])

        it = 0
        for i in range(0, L3):
            for j in range(0, numLink):
                print "\t\t%s -> %s" % (self.switchList[L2+i+1], self.hostList[it])
                self.addLink(self.switchList[L2+i+1], self.hostList[it])
                it+=1
                if (it+1) > numHost:
                    break;


#Add options for user
PARSER =  OptionParser()
PARSER.add_option("-n","--numHost", type="int", dest="host", help="Specify the number of host.", default=8)
PARSER.add_option("-l","--numLink", type="int", dest="link", help="Specify the number of host links per switch", default=2)
PARSER.add_option("-b","--bandwidth", type="int", dest="bandwidth", help="Specify the bandwidth of each link.", default=10)

#Retrieve options from user
(opts, args) = PARSER.parse_args();
HOST = opts.host
LINK = opts.link
BANDWIDTH = opts.bandwidth

def createTopo():
    topo = DynamicTopo(HOST, LINK, BANDWIDTH)
    net = Mininet( topo=topo, switch=OVSBridge)
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createTopo()
