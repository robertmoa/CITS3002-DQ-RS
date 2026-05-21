class Host:
    def __init__(self,name,ip,mac):
        self.name = name
        self.ip = ip
        self.mac = mac


class Router:
    def __init__(self,name):
        self.name = name

        #As the router has 2 i
        #interfaces are ip addresses
        self.interfaces = {}

        #routing tables are ip addresses
        self.routing_table = {}


class Interface:
    def __init__(self,ip,mac):
        self.ip = ip
        self.mac = mac

#routes to subnets
class Route:
    def __init__(self,next_hop,interface):
        self.next_hop = next_hop
        self.interface = interface