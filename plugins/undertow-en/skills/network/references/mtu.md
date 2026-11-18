# MTU

Use this section when there are symptoms like "some sites open, some hang", "slow through the VPN", "QUIC works but TCP breaks" or "large packets disappear".

## Simple explanation

MTU is the maximum size of an IP packet that can be sent over a particular link without fragmentation. MSS is the maximum size of TCP payload inside a segment.

## Technical explanation

MTU is tied to a link or logical interface. For IPv4, fragmentation by routers is possible, though undesirable in practice. For IPv6, routers do not fragment transit packets; correct PMTUD per RFC 8201 and ICMPv6 is critical.

## History

- Classic PMTUD for IPv4 is described in RFC 1191.
- IPv6 PMTUD is described in RFC 8201.
- MSS historically relates to RFC 879 and the evolution of TCP.

## Components

- interface MTU
- IP fragmentation
- the DF bit in IPv4
- ICMP Fragmentation Needed / Packet Too Big
- PMTUD
- TCP MSS

## Common misconceptions

- "Lowering the MTU always makes things better": not always; you can lose throughput.
- "MSS and MTU are the same thing": no, MSS is smaller than MTU because TCP/IP headers take space.
- "ICMP can safely be blocked entirely": this often breaks PMTUD, especially in IPv6.

## MTU, MSS and PMTUD in detail

### RFCs and normative basis

- RFC 879 - TCP MSS
- RFC 1191 - Path MTU Discovery for IPv4
- RFC 4821 - Packetization Layer Path MTU Discovery
- RFC 8201 - Path MTU Discovery for IPv6

### Basic logic

| Term | Meaning |
| --- | --- |
| MTU | The maximum IP packet size on an interface/link |
| MSS | The maximum TCP payload size |
| PMTU | The smallest MTU along the path |
| PMTUD | The mechanism for discovering the PMTU |

### ASCII diagram

```text
host A MTU 1500
  -> router
  -> tunnel segment effective MTU 1420
  -> router sends ICMP too big / fragmentation needed
  -> host reduces packet size or MSS
```

### Practical calculations

```text
Ethernet MTU 1500
IPv4 + TCP: MSS 1460
IPv6 + TCP: MSS 1440
```

### Linux commands

```sh
ip link show
tracepath 1.1.1.1
tracepath6 2606:4700:4700::1111
ping -M do -s 1472 1.1.1.1
ping6 -s 1440 2606:4700:4700::1111
tcpdump -ni any 'icmp or icmp6'
```

### Practical diagnostic examples

#### Checking for an MTU black hole

```sh
ping -M do -s 1472 8.8.8.8
ping -M do -s 1400 8.8.8.8
```

If the large packet does not pass and the smaller one does, there is a narrower MTU along the path or PMTUD is broken.

#### Checking TCP MSS indirectly

Capture the SYN with `tcpdump` and look at the negotiated MSS.

### Real network scenarios

#### Scenario 1. PPPoE + VPN

The outer link already reduces the available payload, and the tunnel overhead is added on top. Without correct MTU/MSS, some sites hang during TLS or when loading large objects.

#### Scenario 2. IPv6 works worse than IPv4

Often the cause is not "bad IPv6" but filtering of ICMPv6 `Packet Too Big`.

### Common mistakes

- Blocking ICMP/ICMPv6 entirely.
- Confusing MTU and MSS.
- Changing the MTU on the client without checking the bottleneck along the path.
- Ignoring the overhead of PPPoE, GRE, VXLAN, WireGuard, OpenVPN, IPsec.

### Diagnostic order

1. Check the interface MTUs.
2. Check the real PMTU with `tracepath`.
3. Check ICMP/ICMPv6 `too big` messages.
4. Compare the behavior of small and large packets.
5. For TCP, look at the negotiated MSS and a possible MSS clamp.

### Cross-references

- Transport and MSS: `tcp-vs-udp.md`
- IPv6 and ICMPv6: `ipv6.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| MTU | The maximum IP packet size on a link | Avoid unsupportedly large packets | Limits the size of the packet sent on an interface | Allows sizes to be matched | A wrong value causes loss | Ethernet MTU 1500 | A home router, PPPoE, a VPN tunnel | Related to PMTUD |
| MSS | The maximum TCP payload size | Avoid unnecessary TCP fragmentation | Negotiated by the TCP peers when the connection is set up | Improves compatibility | Relevant only for TCP | MSS 1460 with MTU 1500 and IPv4 | TCP through a tunnel with an MSS clamp | Derived from MTU |
| PMTUD | Path MTU discovery | Fit the packet size to the path | Uses packet-too-big messages | Improves delivery | Breaks with ICMP filtering | A VPN with a reduced MTU | Some sites hang because of an MTU black hole | Relies on ICMP/ICMPv6 |
| Fragmentation | Splitting a packet into fragments | Allow an oversized packet to be forwarded | A large packet is split into parts | Compatibility in old scenarios | Overhead and loss | IPv4 fragments | Old UDP traffic through a narrow link | Related to MTU |

## Examples

### Example 1. PPPoE

If PPPoE runs on top of Ethernet, the available payload shrinks. The typical MTU becomes smaller than 1500, and if this is not taken into account, some TCP sessions may hang.

### Example 2. WireGuard through a home router

The outer interface has an MTU of 1500, but a tunnel with additional headers runs on top of it. The effective path is smaller than 1500. If the MTU/MSS is not configured correctly, some traffic will suffer loss.

### Example 3. A large ping check

```sh
ping -M do -s 1472 8.8.8.8
tracepath 8.8.8.8
```

If `ping` with `-M do` does not pass and a smaller size does, there is a smaller MTU along the path or ICMP is blocked.

### A real use case

After enabling a tunnel, the user complains: "only simple sites open". Often this is not DNS but exactly an MTU/PMTUD black hole.
