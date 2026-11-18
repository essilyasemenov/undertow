# OSI Model

Use this section when you need to break a network problem down by layer and avoid merging a physical fault, IP routing, DNS and an application protocol into one cause.

## Simple explanation

OSI is a teaching model that divides network communication into 7 layers, to make it easier to see where exactly the connection breaks.

## Technical explanation

OSI does not describe the Internet "as it is implemented byte for byte". It is an ISO abstraction that helps separate physical signal transmission, link-level frame delivery, inter-network packet delivery, transport, sessions, data presentation and applications. In real operation the TCP/IP stack is simpler, but the diagnostic value of OSI remains high.

## History

- Developed by ISO as a reference model for inter-system communication.
- Historically it became a common language for engineers and for teaching networking.
- The modern Internet is built not strictly on OSI but closer to TCP/IP, yet the terms L2, L3, L4 and L7 are used everywhere.

## Layers and typical examples

| Layer | What it does | Examples |
| --- | --- | --- |
| L1 Physical | Transmits bits | cable, fiber, radio channel |
| L2 Data Link | Delivers frames within a segment | Ethernet, Wi-Fi, MAC |
| L3 Network | Delivers packets between networks | IPv4, IPv6, ICMP |
| L4 Transport | Delivers data to processes | TCP, UDP |
| L5 Session | Manages session logic | parts of SMB, RPC, a TLS session in the application context |
| L6 Presentation | Data representation and encoding | TLS, ASN.1, JSON encoding in the practical sense |
| L7 Application | Application logic | HTTP, DNS, SMTP |

## How it works

```text
application
  -> builds the payload
  -> passes it down the stack
  -> each layer adds its own header
  -> at the receiver the headers are removed in reverse order
```

## Main components and tools

- L1: `ethtool`, link indication, SFP/cable tests
- L2: `ip link`, `bridge`, `arp`, `tcpdump -e`
- L3: `ip addr`, `ip route`, `ping`, `traceroute`
- L4: `ss -lntup`, `nc`, `tcpdump 'tcp or udp'`
- L7: `curl`, `dig`, `openssl s_client`

## Common mistakes and misconceptions

- "Ping works, so the network is fine": no, DNS, TCP/443 or MTU may be broken.
- "OSI matches the Internet exactly": no, it is a model, not a literal implementation.
- "DNS is always a separate layer": in practice DNS is considered an application, although it depends on L3/L4.

## Best practices

- Diagnose bottom-up: link -> L2 -> IP -> route -> transport -> application.
- State the problem by layer: "no carrier", "no ARP", "no default route", "TCP SYN goes out without a SYN-ACK", "DNS answers NXDOMAIN".
- Use OSI as a common language, not as dogma.

## Sources

- Cloudflare Learning Center: OSI Model
- Cisco Networking Academy: CCNA Introduction to Networks

## OSI in detail

### The role of this section

This section is not for describing a specific Internet standard but for methodically breaking a fault down by layer. Details of TCP/IP, DNS, MTU, NAT and routing are in the dedicated sections.

### RFCs and normative basis

- There is no RFC for the OSI model itself: it is an ISO reference model.
- RFC 1122 - Host Requirements and the practical layer model of the TCP/IP stack.
- RFC 1123 - additional requirements for hosts and application protocols.

### OSI versus TCP/IP

| OSI | TCP/IP | What is actually diagnosed |
| --- | --- | --- |
| L7-L5 | Application | DNS, HTTP, TLS, SSH |
| L4 | Transport | TCP, UDP, ports, retransmission |
| L3 | Internet | IPv4, IPv6, routing, ICMP |
| L2-L1 | Link | Ethernet, Wi-Fi, VLAN, carrier |

### ASCII diagram

```text
L7  Application   -> HTTP, DNS, SMTP
L6  Presentation  -> TLS, data encoding
L5  Session       -> managing the exchange logic
L4  Transport     -> TCP, UDP, ports
L3  Network       -> IPv4, IPv6, routing
L2  Data Link     -> Ethernet, Wi-Fi, MAC, VLAN
L1  Physical      -> cable, fiber, radio
```

### Practical diagnostic diagram

```text
no access to the service
  -> is there carrier/L1
  -> is there adjacency and VLAN/L2
  -> is there an address, a route and a gateway/L3
  -> is there a TCP/UDP exchange/L4
  -> do DNS/TLS/HTTP/L7 work
```

### Linux commands

```sh
ip link
ip addr
bridge link
ip route
ping -c 3 8.8.8.8
traceroute 8.8.8.8
ss -lntup
tcpdump -ni any
curl -I https://example.com
dig example.com
```

### Real scenarios

#### Scenario 1. "Wi-Fi is up, sites do not open"

- L1/L2: the association exists.
- L3: the client got an address, but there is no default route.
- Conclusion: an L3 problem, not "the Internet is broken in general".

#### Scenario 2. "The IP pings, the name does not resolve"

- L3 is fine.
- L7 for DNS is broken.
- Conclusion: there is no need to start with the cable or the route.

#### Scenario 3. "The service listens locally but is unreachable from outside"

- L4 on the host may be fine.
- The problem may be at the L3/L4 boundary: firewall, NAT, return route.

### Common mistakes

- Trying to explain any failure by a single layer.
- Treating OSI as a literal map of the modern Internet.
- Concluding "the network is fine" from `ping` alone.
- Analyzing DNS before checking the IP address and route.

### Diagnostic order

1. Check the physical state of the interface and the carrier.
2. Check L2 adjacency: MAC, bridge, VLAN, ARP/NDP.
3. Check L3: address, prefix, route selection, gateway.
4. Check L4: SYN/SYN-ACK, UDP request and response, the listening socket.
5. Check L7 with a specific client: `curl`, `dig`, `openssl s_client`.

### Cross-references

- The real Internet stack: `tcp-ip.md`
- Transport: `tcp-vs-udp.md`
- Addressing and routes: `ipv4.md`, `ipv6.md`, `routing.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Relation to other technologies |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OSI | The 7-layer reference model | Simplify network analysis | Divides functions into abstract layers | A common language for engineers | Not a literal implementation of the Internet | Analysis like "this is an L3 problem, not DNS" | Mapped to the TCP/IP stack |
| L2 | The data link layer | Delivery within a segment | Frames, MAC, VLAN | Fast local delivery | Does not solve inter-network routing | A switch forwards an Ethernet frame | The basis for ARP, bridge, Wi-Fi |
| L3 | The network layer | Delivery between networks | IP addressing and routing | Scalability | Depends on a correct route | A packet goes out through the default gateway | The basis for TCP, UDP, ICMP |
| L4 | The transport layer | Delivery to a process/socket | Ports, segments, datagrams | Demultiplexing services | Does not solve naming and routing | TCP/443 and UDP/53 | Relies on IP |
| L7 | The application layer | Implementing service logic | Application protocols | Functionality visible to the user | Strongly depends on the lower layers | HTTP, DNS, SMTP | Uses TCP/UDP and IP |

## Examples

### Scenario 1. "Wi-Fi is up, the Internet does not work"

Layer by layer:

1. L1/L2: the client is associated with Wi-Fi, there is a link.
2. L3: the client got the address `192.168.1.20/24`, but the gateway is wrong.
3. L4/L7: not checked until L3 is fixed.

Conclusion: the symptom looked like "the Internet died", but the root cause is an addressing error.

### Scenario 2. "The IP pings, but the site does not open"

```text
ping 1.1.1.1            -> works
dig example.com         -> timeout
curl https://1.1.1.1    -> TCP works, but that does not mean the needed site is reachable
```

Conclusion: most likely the problem is in L7/L4 for DNS, not in basic IP connectivity.

### Scenario 3. "The service listens but is unreachable from outside"

- L4 locally: `ss -lntp` shows `0.0.0.0:443`
- L3: there is a route out
- L4/L3 at the border: the firewall or NAT does not pass the incoming SYN

### Frequent questions

#### Where to start diagnostics?

From the lowest layer you can confirm. If there is no link, analyzing DNS is pointless.

#### When is the OSI model harmful?

When it is used as dogma and the real stack specifics of TCP/IP, QUIC, NAT and firewall state are ignored.
