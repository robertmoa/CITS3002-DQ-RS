from protocol import EthernetFrame, IPPacket, UDPSegment
from config import MAX_SEGMENT_SIZE, TTL_DEFAULT, host_a_mac, host_a_ip, host_b_ip, host_b_mac, r1_iface1_ip, r1_iface1_mac, r1_iface2_ip, r1_iface2_mac

class Host:
    def __init__(self,name,ip,mac,src_port,dst_port):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.src_port = src_port
        self.dst_port = dst_port
        self.mac_table = {}
        self.routing_table = {}
        self.last_ack = None

    def send(self, dst_ip, data, network):
        if isinstance(data, str):
            data = data.encode()
        
        chunks = [data[i:i + MAX_SEGMENT_SIZE] for i in range(0, len(data), MAX_SEGMENT_SIZE)]

        seq = 0
        for chunk in chunks:
            print(f"{self.name}: Layer 4: Data received from Application Layer. Data size={len(chunk)}")
            self._l4_send(dst_ip, chunk, seq)
            seq ^= 1

    def _l4_send(self, dst_ip, chunk, seq):
        while True:
            segment = UDPSegment(self.src_port, self.dst_port, UDPSegment.DATA, seq, chunk)
            print(f"{self.name}: Layer 4: Checksum computed")
            print(f"{self.name}: Layer 4: Segment created by adding transport layer header (DATA, seq=0) (encapsulation)")
            print(f"{self.name}: Layer 4: Segment sent to Network Layer")

            self.last_ack = None
            self._l3_send(dst_ip, segment)
    def _l3_send(self, dst_ip, segment):
        packet = IPPacket(self.ip, dst_ip, TTL_DEFAULT, IPPacket.PROTOCOL_UDP, segment)
        print(f"{self.name}: Layer 3: Segment received from Transport Layer: SRC_IP={self.ip}, DST_IP={dst_ip}, TTL={packet.ttl}")
        print(f"{self.name}: Layer 3: Destination IP read: {dst_ip}")

        next_hop = self._route_lookup(dst_ip)
        print(f"{self.name}: Layer 3: Routing table lookup performed")
        print(f"{self.name}: Layer 3: Next-hop IP determined: {next_hop}")
        print(f"{self.name}: Layer 3: Outgoing interfact selected")
        print(f"{self.name}: Layer 3: Packet forwarded to Data Link Layer")

        self._l2_send(next_hop, packet)


    def _route_lookup(self, dst_ip):
        for network, next_hop in self.routing_table.items():
            if self._in_network(dst_ip, network):
                if next_hop == "direct":
                    return dst_ip
                return next_hop
        return self.routing_table.get("default")

    def _in_network(self, ip, network):
        if network == "default":
            return False
        net_prefix = network.split("/")[0].rsplit(".", 1)[0]
        ip_prefix = ip.rsplit(".", 1)[0]
        return net_prefix == ip_prefix


    def _l2_send(self, next_hop_ip, packet):
        pass
    def receive(self, frame, network=None):
        pass

    def _l2_receive(self, frame, network):
        pass

    def _l3_receive(self, packet, network):
        pass

    def _l4_receive(self, segment, src_ip, network):
        pass


class Router:
    def __init__(self,name):
        self.interfaces = {}
        self.routing_table = {}
        self.mac_table = {}
    
    def receive(self, frame, in_interface, network):
        pass

    def _l2_receive(self, frame, in_interface, network):
        pass

    def _l3_receive(self, packet, in_interface, network):
        pass

    def _l2_send(self, next_hop_ip, out_interface, packet, network):
        pass


class Interface:
    def __init__(self,ip,mac):
        self.ip = ip
        self.mac = mac

#routes to subnets
class Route:
    def __init__(self,next_hop,interface):
        self.next_hop = next_hop
        self.interface = interface



#the actual setup of the devices
hostA = Host("Host-A",host_a_ip,host_a_mac,)

hostB = Host("Host-B",host_b_ip,host_b_mac)

router = Router("R-1")
router.interfaces = {
    "i1": Interface(r1_iface1_ip,r1_iface1_mac),
    "i2": Interface(r1_iface2_ip,r1_iface2_mac)

}
router.routing_table = {
"10.0.1.0/24": Route(r1_iface1_ip,router.interfaces["i1"]),
"10.0.2.0/24": Route(r1_iface2_ip,router.interfaces["i2"])
}