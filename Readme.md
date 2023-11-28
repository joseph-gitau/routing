# Routing Simulation

This project simulates a network of routers through socket programming, showcasing how routers route traffic across the Internet.

## Overview

Each router creates connections to neighboring routers based on a given topology, forming a network of routers. One router reads an input file containing packets to be routed across this network. This router sends each packet to the appropriate next-hop router, determined by its forwarding table. The next-hop router then forwards the packet to its appropriate next-hop. This process continues until each packet reaches its final hop router.

### Inputs

1. **Packets File (packets.csv):**
    - Contains simplified packet data (source IP, destination IP, payload, TTL).
    - Each line: `source IP, destination IP, payload, TTL`.
    
2. **Forwarding Table per Router (router_#_table.csv):**
    - Each router has its own forwarding table.
    - Table fields: network destination, netmask, gateway, interface.

3. **Router Network Topology Diagram:**
    - Displays routers (1 to 6) and their interfaces.

## Instructions and Hints

### Abstractions

- Each interface is represented by a port.
- Actual IP address of each router is 127.0.0.1.
- Simulated IP addresses in forwarding tables represent the routers.
- Each interface corresponds to a unique IP address.

### Setup

- Each router is a separate program running on 127.0.0.1.
- Routers use sockets for communication.
- Determine which routers act as clients, servers, or both.

### Routing Process

1. **Receive Packets:**
    - Routers append received packets to `received_by_router_#.txt`.

2. **Routing Logic:**
    - Parse packets for destination IP and TTL.
    - Match destination IP in forwarding table.
    - Determine the next hop based on forwarding rules.
    - Decrement TTL. Discard packets if TTL = 0.
    - Forward packets or append payload to `out_router_#.txt`.

## Running the Network

1. Open 6 separate terminal windows.
2. Run each router program in reverse order according to the network topology (e.g., router6.py, router5.py, ...).

### Notes

- Use Python for ease of socket programming and threading.
- Only permitted to use specified Python libraries or equivalent libraries in other languages.

