import sys
from devices import hostA, hostB, router
from config import host_b_ip

if len(sys.argv) != 2:
    print("Usage: python main.py <message_size_in_bytes>")
    sys.exit(1)

size = int(sys.argv[1])
data = b"X" * size  # filler payload of the requested size
hostA.send(host_b_ip, data)