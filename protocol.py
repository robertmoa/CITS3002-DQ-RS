class EthernetFrame:
    """
    Layer 2 Ethernet ish frame. Refer to L3P7 for format
    The fields should look like
    Fields:
        dst_mac (str) : Destination MAC example (BB:BB:BB:BB:BB:BB)
        src_mac (str) : Source Mac      example (AA:AA:AA:AA:AA:AA)
        etype   (int) : EtherType, should always 0x0800 (IPv4) format for this project
        payload       : The IPPacket itself wrapped within this frame
    """

    """decision to hard code to IPv4"""
    ETPYE_IPV4 = 0x0800

    def __init__(self, dst_mac, src_mac, etype, payload)
        self.dst_mac = dst_mac
        self.src_mac = src_mac
        self.etype   = etype
        self.payload = payload

class IPPacket:
    """Layer 3 Simulation of a packet
    Fields:
        src_ip    (str) : Source      IP Address example "10.0.1.12"
        dst_ip    (str) : Destination IP Address example "10.0.2.22"
        ttl       (int) : Time to live, starts a counter from 100, then decrements.
        protocol  (int) : 17 = UDP-like payload
        payload         : The UDPSegment object wrapped inside this packet
    """
    
    PROTOCOL_UDP = 17

    def init(self, src_ip, dst_ip, ttl, protocol, payload):
        self.src_ip   = src_ip
        self.dst_ip   = dst_ip
        self.ttl      = ttl
        self.protocol = protocol
        self.payload  = payload
    pass

class UDPSegment:
    """need to write the layer 4 UDP segment with rdt2.2 ACK support, checksum is gonna be fked"""
    pass
