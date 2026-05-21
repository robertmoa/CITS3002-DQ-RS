from devices import Host,Router,Interface,Route


network1 = "10.0.1.0/24"
network2 = "10.0.2.0/24"

host_a_ip = "10.0.1.10"
host_b_ip = "10.0.2.20"

r1_iface1_ip = "10.0.1.1"   # Router R1, subnet 1 side
r1_iface2_ip = "10.0.2.1"   # Router R1, subnet 2 side


host_a_mac = "AA:AA:AA:AA:AA:AA"
host_b_mac = "DD:DD:DD:DD:DD:DD"

r1_iface1_mac = "BB:BB:BB:BB:BB:BB"
r1_iface2_mac = "CC:CC:CC:CC:CC:CC"

TTL_DEFAULT = 100
MAX_SEGMENT_SIZE = 500  # bytes, the max 500 req





