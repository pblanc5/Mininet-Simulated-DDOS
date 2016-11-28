#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.util import irange,dumpNodeConnections
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

    #Builds the network
    def __init__( self, numHost, numLink, bandwidth ):
        "Create custom topo."
        Topo.__init__( self )

        #Switch Layers
        L3 = int(math.ceil(float(numHost)/numLink))
        L2 = int(math.ceil(float(numLink)/L3))
        L1 = 1

        #Add Hosts
        self.hostList.append(self.addHost('h1'))
        for i in range(1, numHost):
            self.hostList.append(self.addHost('h%d' % (i+1), cpu= .001))
        #Add Switches
        for i in range(0, L2+L3+L1):
            self.switchList.append(self.addSwitch('s%d' % (i+1)))

        #Set links
        #L1 > L2
        for i in range(0, L2):
            self.addLink(self.switchList[0], self.switchList[L1+i])

        #L2 -> L3
        for i in range(0, L2):
            for j in range(0, L3):
                self.addLink(self.switchList[L1+i], self.switchList[L2+j+1])

        #L3 -> H
        it = 0
        for i in range(0, L3):
            for j in range(0, numLink):
                if(self.hostList[it] == "h1"):
                    self.addLink(self.switchList[L2+i+1], self.hostList[it], bw=bandwidth)
                else:
                    self.addLink(self.switchList[L2+i+1], self.hostList[it])
                it+=1
                if (it+1) > numHost:
                    break


#Add options for user
PARSER =  OptionParser()
PARSER.add_option("-n","--numHost", type="int", dest="host", help="Specify the number of host.", default=8)
PARSER.add_option("-l","--numLink", type="int", dest="link", help="Specify the number of host links per switch", default=2)
PARSER.add_option("-b","--bandwidth", type="int", dest="bandwidth", help="Specify the bandwidth of each link.", default=1)
PARSER.add_option("-a", "--attack", type="str", dest="attack", help="Specify the attack on the victim machine. Takes: UDP, TCP, ARP", default="UDP")

#Retrieve options from user
(opts, args) = PARSER.parse_args();
HOST = opts.host
LINK = opts.link
BANDWIDTH = opts.bandwidth
ATTACK = opts.attack
ATTACK_OPTS = ["UDP", "TCP", "ARP"]

#Sets up the Host to run scripts
def initHost(hostList, net, opt):
    victimScriptList = ["udp_victim.py", "tcp_victim.py", "arp_victim.py"]
    attackScriptList = ["udp_attack.py", "tcp_attack.py", "arp_attack.py"]

    #Script to run
    VICTIM_SCRIPT = "python " + victimScriptList[opt]
    ATTACKER_SCRIPT = "python " + attackScriptList[opt]

    victim = net.get(hostList[0])
    victim_ip = victim.IP()
    victim_mac = victim.MAC()

    #init victim
    try:
        command = VICTIM_SCRIPT + " " + victim.MAC() + " " + victim.IP() + " > victim_log &"
        victim.cmd(command)
        print "[+] Starting Victim Script"
    except:
        print "[-] Starting Victim Script"

    #init attackers
    for i in range(1, len(hostList)):
        host = net.get(hostList[i])
        host_ip = "10.0.0.1"
        host_mac = host.MAC()
        try:
            command = ATTACKER_SCRIPT + " " + host.MAC() + " 10.0.0.1  > attacker_log &"
            host.cmd(command)
            print "[+] Starting Attack Script for " + hostList[i]
        except:
            print "[-] Starting Attack Script for " + hostList[i]

def createTopo():
    topo = DynamicTopo(HOST, LINK, BANDWIDTH)
    net = Mininet( topo=topo, switch=OVSBridge, link=TCLink)
    net.start()
    initHost(topo.hostList, net, ATTACK_OPTS.index(ATTACK))
    print "Starting network: host=" + str(HOST) + " link=" + str(LINK) + " bandwidth=" + str(BANDWIDTH) + " attack=" + str(ATTACK)
    CLI(net)
    net.iperf()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createTopo()
