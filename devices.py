from protocol import EthernetFrame, IPPacket, UDPSegment
import config

class Host:
    def __init__(self, name, ip, mac, src_port, dst_port):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.src_port = src_port
        self.dst_port = dst_port
        self.mac_table = {}
        self.routing_table = {}

    def send(self, dst_ip, data, network):
        if isinstance(data, str):
            data = data.encode()
        
        chunks = [data[i:i + config.MAX_SEGMENT_SIZE] for i in range(0, len(data), config.MAX_SEGMENT_SIZE)]

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

    def _l3_send(self, dst_ip, segment, network):
        pass

    def _l2_send(self, next_hop_ip, packet, network):
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
    def __init__(self, name, interfaces, routing_table, mac_table):
        self.name = name
        self.interfaces = interfaces
        self.routing_table = routing_table
        self.mac_table = mac_table
    
    def receive(self, frame, in_interface, network):
        pass

    def _l2_receive(self, frame, in_interface, network):
        pass

    def _l3_receive(self, packet, in_interface, network):
        pass

    def _l2_send(self, next_hop_ip, out_interface, packet, network):
        pass
