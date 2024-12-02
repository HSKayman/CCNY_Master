from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import Node
from mininet.node import OVSController
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import dumpNodeConnections

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params) # changing
        self.cmd("sysctl net.ipv4.ip_forward=1") # changing
        
    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0") # changing
        super(LinuxRouter, self).terminate() # changing

class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add routers with explicit subnets
        routers = {}
        for i in range(1, 8):
            routers[f'r{i}'] = self.addHost(
                f'r{i}', 
                cls=LinuxRouter, 
                ip=f'10.0.{i}.1/24'
            )

        # Add switches
        switches = {}
        for i in range(1, 7):
            switches[f's{i}'] = self.addSwitch(f's{i}')

        # Link configuration using pfifo instead of htb
        base_link_params = {
            'delay': '1ms',
            'use_htb': False,
            'use_pfifo': True,
            'max_queue_size': 1000
        }

        # Connect routers to switches with simpler configuration
        for i in range(1, 7):
            link_params = base_link_params.copy()
            link_params['ip'] = f'10.0.{i}.1/24'
            self.addLink(
                routers[f'r{i}'],
                switches[f's{i}'],
                intfName1=f'r{i}-eth0',
                params1=link_params,
                cls=TCLink
            )
        
        # Connect r7 to s1
        link_params = base_link_params.copy()
        link_params['ip'] = '10.0.7.1/24'
        self.addLink(
            routers['r7'],
            switches['s1'],
            intfName1='r7-eth0',
            params1=link_params,
            cls=TCLink
        )

        # Router links with explicit subnets using simpler queueing
        router_links = [
            (('r1', 'r2'), 900, '10.100'),
            (('r1', 'r5'), 700, '10.101'),
            (('r1', 'r7'), 200, '10.102'),
            (('r2', 'r3'), 300, '10.103'),
            (('r3', 'r4'), 200, '10.104'),
            (('r3', 'r6'), 400, '10.105'),
            (('r4', 'r5'), 400, '10.106'),
            (('r6', 'r7'), 200, '10.107')
        ]

        # Counter for router interfaces
        intf_count = {}
        for r in routers:
            intf_count[r] = 1

        # Add router-to-router links with simplified queueing
        for (r1, r2), bw, subnet in router_links:
            r1_intf = intf_count[r1]
            r2_intf = intf_count[r2]
            intf_count[r1] += 1
            intf_count[r2] += 1
            
            params1 = base_link_params.copy()
            params2 = base_link_params.copy()
            params1['ip'] = f'{subnet}.1/24'
            params2['ip'] = f'{subnet}.2/24'

            self.addLink(
                routers[r1],
                routers[r2],
                intfName1=f'{r1}-eth{r1_intf}',
                intfName2=f'{r2}-eth{r2_intf}',
                params1=params1,
                params2=params2,
                bw=bw,
                cls=TCLink
            )

        # Add switch interconnections
        for i in range(1, 6):
            self.addLink(
                switches[f's{i}'],
                switches[f's{i+1}'],
                cls=TCLink,
                **base_link_params)

def configure_network(net):
    info('*** Configuring routers\n')
    
    # Configure each router's routing
    for i in range(1, 8):
        router = net[f'r{i}']
        
        # Add routes to other subnets
        for j in range(1, 8):
            if i != j:
                router.cmd(f'ip route add 10.0.{j}.0/24 via 10.0.{i}.1')

def run():
    topo = NetworkTopo()
    net = Mininet(
        topo=topo,
        controller=OVSController, # changing
        link=TCLink
    )
    
    net.start()
    
    info('*** Configuring network\n')
    configure_network(net)
    
    info('*** Testing network connectivity\n')
    net.pingAll()
    
    info('*** Routing tables on routers:\n')
    for i in range(1, 8):
        router = net[f'r{i}']
        info(f'\n{router.name}:\n')
        info(router.cmd('route -n'))
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()