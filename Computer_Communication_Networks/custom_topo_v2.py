#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, OVSKernelSwitch, RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
import os

class CustomSDNTopology(Topo):
    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Add links with different capacities and delays
        self.addLink(h1, s1, bw=10, delay='5ms')
        self.addLink(h2, s2, bw=10, delay='5ms')
        self.addLink(h3, s3, bw=10, delay='5ms')
        self.addLink(h4, s4, bw=10, delay='5ms')
        
        # Inter-switch links
        self.addLink(s1, s2, bw=5, delay='10ms')
        self.addLink(s2, s3, bw=5, delay='10ms')
        self.addLink(s3, s4, bw=5, delay='10ms')
        self.addLink(s4, s1, bw=5, delay='10ms')
        self.addLink(s1, s3, bw=5, delay='10ms')

def run_network():
    # Create network with remote controller
    topo = CustomSDNTopology()
    net = Mininet(topo=topo, 
                  host=CPULimitedHost, 
                  link=TCLink, 
                  switch=OVSKernelSwitch,
                  controller=RemoteController)
    
    # Start network
    net.start()
    
    # Print connections
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    
    # Start CLI
    CLI(net)
    
    # Stop network
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_network()