# CITS3002 Project - Mini Internet Protocol Stack Simulation
**Authors:** Robert Smart (24468811), Dennis Quek (23879473)

A Python simulation of L2/L3/L4 networking. Sends data from Host A -> Router R1 -> Host B across two /24 subnets, with framing, routing, TTL, segmentation, checksums, and rdt2.2 ACKS.

## Run

```bash
python main.py (data size in bytes)
```

Example:
```bash
python main.py 100   # Runs a single segment
python main.py 1200  # Runs three segments (500 bytes, 500 bytes, then 200 bytes)
```

Output is a per-layer log of every step. Matching word for word format to the specification provided.

## Topology

Subnet 1: `10.0.1.0/24`  
Subnet 2: `10.0.2.0/24`  
MACs and routing tables are hardcoded in `config.py` and `devices.py`.

| File | Purpose |
|---|---|
| `main.py` | Entry point. Takes message size from CLI, calls `hostA.send()`. |
| `config.py` | Fixed constants: IPs, MACs, TTL default, max segment size (500). |
| `protocol.py` | Header classes: `EthernetFrame` (L2), `IPPacket` (L3), `UDPSegment` (L4). UDP includes the 16-bit 1's complement checksum and rdt2.2 seq/ACK fields. |
| `devices.py` | `Host`, `Router`, `Interface`, `Route`, `SubNetLink` classes, plus the topology setup at the bottom. |

## How it works (shortened)

**L4 (Transport).** `Host.sends()` splits the message into ≤500-byte chunks. Each chunk becomes a `UDPSegment` with a sequence number alternating 0/1. Checksum is computed over powers + length + type + seq + payload using 16-bit 1's complement with carry wraparound. Sender blocks until the matching ACK arrives, on wrong/no ACK, it retransmits the same seq.

**L3 (Network).** The segment is wrapped in an `IPPacket` with src/dst IP and TTL=100. Each device runs a longest-prefix-ish lookup against its routing table (a direct route returns the destination IP itself as next-hop; otherwise the next-hop IP is the router interface) The router decrements TTL on every packet and drops at zero.

**L2 (Data Link).** The packet is wrapped in an `EthernetFrame` with src/dst MAC. The next-hop IP is mapped to a MAC via the device's MAC table (hardcoded, acts as a startic ARP). Frames are delivered over `SubNetLink`, which dispatches to the device whose MAC matches the frame's destination. Frames not addressed to the receiver are dropped.

**Reliable delivery (rdt2.2)** Receiver verifies the checksum; corrupted segments are discarded and the last good ACK is re-sent. Duplicate seq -> re-ACK without redelivery, Sender blocks on `last_ack` and retransmits on wrong/missing ACK.

## Assumptions

- Simulation is synchronous: an ACK comes back up the call stack before `_l4_send` checks `last_ack`. No threading nor timer needed.
- Another assumption since the testing mention was using `python main.py 100`, we assume that `TTL=1` would not be a method of testing for <=0 for it.