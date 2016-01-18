from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.topo import Topo

class Topology( Topo ):
    "Custom topology script."

    def __init__( self ):
        "Creating topology."
        Topo.__init__( self )

        
        h1 = self.addHost( 'h1' )
        h2 = self.addHost( 'h2' )
        h3 = self.addHost( 'h3' )
	h4 = self.addHost( 'h4' )
	h5 = self.addHost( 'h5' )
	h6 = self.addHost( 'h6' )
        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
	s4 = self.addSwitch( 's4' )
	s5 = self.addSwitch( 's5' )
	s6 = self.addSwitch( 's6' )
	s7 = self.addSwitch( 's7')        
        self.addLink(s1,h1,port1=1)
        self.addLink(s2,h2,port1=1)
        self.addLink(s3,h3,port1=1)
	self.addLink(s4,h4,port1=1)
	self.addLink(s5,h5,port1=1)
	self.addLink(s6,h6,port1=1)
	self.addLink(h1,s7,port1=1)
        self.addLink(s1,s2)
        self.addLink(s2,s3) 
	self.addLink(s3,s4)
	self.addLink(s4,s5)
	self.addLink(s5,s6)
        self.addLink(s6,s7)

	   
topos = { 'create_topo': ( lambda: Topology() ) }
