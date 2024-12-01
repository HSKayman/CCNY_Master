#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch

class CustomTopology(Topo):
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
        # Format: (bandwidth in Mbps, delay in ms)
        self.addLink(h1, s1, bw=10, delay='5ms')
        self.addLink(h2, s2, bw=10, delay='5ms')
        self.addLink(h3, s3, bw=10, delay='5ms')
        self.addLink(h4, s4, bw=10, delay='5ms')
        
        # Inter-switch links with different capacities
        self.addLink(s1, s2, bw=5, delay='10ms')
        self.addLink(s2, s3, bw=5, delay='10ms')
        self.addLink(s3, s4, bw=5, delay='10ms')
        self.addLink(s4, s1, bw=5, delay='10ms')  # Creating a ring topology
        self.addLink(s1, s3, bw=5, delay='10ms')  # Cross link for alternative paths

def run_network():
    # Create network
    topo = CustomTopology()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, switch=OVSKernelSwitch)
    
    # Start network
    net.start()
    
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    
    # Start CLI
    CLI(net)
    
    # Stop network
    net.stop()

setLogLevel('info')
run_network()