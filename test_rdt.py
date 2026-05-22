# local testing only, NO SUBMITTTT
from devices import hostA, hostB, router, SubNetLink
from config import host_b_ip
from protocol import UDPSegment

original_transmit = SubNetLink.transmit
data_count = [0]

def corrupting_transmit(self, frame):
    segment = frame.payload.payload  # frame -> packet -> segment
    if segment.seg_type == UDPSegment.DATA:
        if data_count[0] == 0:
            print("*** TEST: corrupting first DATA segment in flight ***")
            # Flip a bit in payload, leave stored checksum alone
            b = bytearray(segment.data)
            if b:
                b[0] ^= 0x01
            segment.data = bytes(b)
        data_count[0] += 1
    original_transmit(self, frame)

SubNetLink.transmit = corrupting_transmit

hostA.send(host_b_ip, b"X" * 10)