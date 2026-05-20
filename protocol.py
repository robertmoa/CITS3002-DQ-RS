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

    def __init__(self, dst_mac, src_mac, etype, payload):
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

    def __init__(self, src_ip, dst_ip, ttl, protocol, payload):
        self.src_ip   = src_ip
        self.dst_ip   = dst_ip
        self.ttl      = ttl
        self.protocol = protocol
        self.payload  = payload
    
    @property
    def total_length(self):
        """
        Total packet size in bytes, since we know IP Header is fixed to 10b, 4,4,1,1
        """
        IP_HEADER_SIZE = 10
        return IP_HEADER_SIZE + self.payload.length



class UDPSegment:
    """need to write the layer 4 UDP segment with rdt2.2 ACK support, checksum is gonna be fked
    From L8P14, UDP is src_port | dst_port | length | checksum, 8 bytes + seg_type and seq so 10b.
    Fields:
        src_port  (int)   : Source port e.g. 5000
        dst_port  (int)   : Destination port e.g. 80
        seg_type  (int)   : 0 = DATA, 1 = ACK
        seq       (int)   : Sequence number - it should be alternating 0 -> 1 -> 0
        data      (bytes) : Application payload 
        checksum  (int)   : 16-bit 1's complement checksum, computed on creation

    Header size: 10 bytes total
    src_port   2 bytes
    dst_port   2 bytes
    seg_type   2 bytes
    seq        2 bytes
    data       1 bytes
    checksum   1 bytes
    """
    DATA = 0
    ACK =  1

    def __init__(self, src_port, dst_port, seg_type, seq, data=b""):
        self.src_port = src_port
        self.dst_port = dst_port
        self.seg_type = seg_type
        self.seq      = seq
        self.data     = data
        self.checksum = self.compute_checksum()

    @property
    def length(self):
        HEADER_SIZE = 10
        return HEADER_SIZE + len(self.data)
    
    def compute_checksum(self):
        values = [
            self.src_port,
            self.dst_port,
            self.length,
            self.seg_type,
            self.seq,
        ]
        data = self.data
        if len(data) % 2 != 0:
            data = data + b'\x00'

        for i in range(0, len(data), 2):
            word = (data[i] << 8) + data[i + 1]
            values.append(word)

        total = sum(values)

        # Carry wraparound
        while total > 0xFFFF:
            total = (total & 0xFFFF) + (total >> 16)

        # 1's complement flip
        return total ^ 0xFFFF

    def verify_checksum(self):
        """
        Recomputes checksum from scratch and compares to stored value.
        Returns True if valid, False if corrupted.
        """
        stored = self.checksum
        self.checksum = 0
        recomputed = self.compute_checksum()
        self.checksum = stored
        return recomputed == stored

