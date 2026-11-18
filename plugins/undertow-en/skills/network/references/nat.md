# NAT

Use this section when you need to explain why an internal address is not visible on the Internet, how Internet access from a private network works, and why inbound connections do not arrive without additional configuration.

## Simple explanation

NAT translates one IP address into another. Most often a home router replaces the client's private IPv4 address with one public address on the WAN.

## Technical explanation

Traditional NAT is described in RFC 3022. In practice NAPT/PAT is more common: translating not only the address but also the transport port, so that many internal hosts can share one external IPv4 address.

## History

- Mass adoption of NAT is linked to the shortage of IPv4 addresses.
- RFC 1918 established the private IPv4 ranges.
- RFC 3022 describes traditional NAT and its operational limitations.

## Components

- private IPv4
- public IPv4
- translation table
- state timeout
- source NAT
- destination NAT
- PAT/NAPT

## Common mistakes

- "NAT = firewall": no, these are different functions, although they are often implemented together.
- "A port forward always solves the problem": no, not if there is a second NAT, CGNAT or a broken route back.
- "IPv6 always needs NAT too": as a rule, no.

## NAT and PAT in detail

### RFCs and normative basis

- RFC 1918 - private IPv4
- RFC 2663 - NAT terminology
- RFC 3022 - Traditional NAT
- RFC 4787 - NAT behavioral requirements for UDP
- RFC 5382 - NAT behavioral requirements for TCP

### Key forms of NAT

| Term | What changes | Typical case |
| --- | --- | --- |
| SNAT | Source address | LAN access to the Internet |
| DNAT | Destination address | Publishing an internal service |
| PAT/NAPT | Source/destination port + address | Many clients behind one IPv4 |

### PAT ASCII diagram

```text
192.168.1.10:51514
  -> router NAT
203.0.113.5:40001
  -> 93.184.216.34:443

reply:
93.184.216.34:443
  -> 203.0.113.5:40001
  -> router translates back
  -> 192.168.1.10:51514
```

### DNAT ASCII diagram

```text
internet client -> 203.0.113.5:443
  -> DNAT on edge router
  -> 192.168.1.20:443
```

### Linux commands

```sh
ip addr
ip route
ss -lntup
tcpdump -ni any host <public-ip>
nft list ruleset
conntrack -L
```

### Practical diagnostic examples

#### Outbound connections work, inbound do not

Check:

1. whether there is DNAT;
2. whether the firewall allows the traffic in the forward and input chains;
3. whether the service listens on the needed address/port;
4. whether the return path is correct.

#### Hairpin NAT

A client in the LAN accesses a service by its public address. If reflection is not configured, the service works from outside but not from inside by the public IP.

### Real network scenarios

#### Scenario 1. A home router publishes a NAS

All of these are needed at once:

- a public IPv4;
- DNAT;
- an allowing firewall;
- a service listening on the needed address;
- a correct route back.

#### Scenario 2. Corporate outbound through SNAT

Internal servers go out under the shared firewall address, and the external system sees the border address rather than the real hosts.

### Common mistakes in practice

- Treating NAT and the firewall as the same thing.
- Forgetting about the return route.
- Confusing DNAT for publishing with SNAT for outbound.
- Looking for the cause only on the server, ignoring the NAT boundary.

### Diagnostic order

1. Determine where exactly NAT is performed.
2. Map the private and public address and port.
3. Check the SNAT/DNAT rules.
4. Check conntrack/state.
5. Check the return route and the application's bind/listen.

### Cross-references

- IPv4 and private ranges: `ipv4.md`
- Provider NAT: `cgnat.md`
- Ports and services: `ports.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| NAT | Address translation | Join different address spaces | A packet passes through a device that changes IP fields and keeps state | Saves IPv4 | Breaks end-to-end | A home router | A LAN reaches the Internet through one WAN IP | Related to IPv4 |
| PAT/NAPT | Address and port translation | Share one public IPv4 among many hosts | Changes the source IP and source port according to the translation table | Very efficient | Harder to debug | `192.168.1.10:51514 -> 203.0.113.5:40001` | Several clients open HTTPS at the same time | A special case of NAT |
| SNAT | Rewriting the source address | Give a client a way out | Changes the source address on the way out | Simple outbound | Does not solve inbound | MASQUERADE on the WAN | A home client opens a site | Uses routing |
| DNAT | Rewriting the destination address | Publish an internal service | Changes the destination address of an incoming packet | Enables inbound | Needs a firewall and a route back | Port forward 443 -> 192.168.1.20 | A home server is published to the outside | Often combined with PAT |

## Examples

### Example 1. A home network

Ten devices with addresses from `192.168.1.0/24` reach the Internet through one public provider address. PAT is performed at the border.

### Example 2. Publishing a web server

```text
203.0.113.5:443
  -> DNAT
192.168.1.20:443
```

For this to work, you need:

- correct DNAT;
- the firewall allowing the inbound traffic;
- a return route through the same router.

### Frequent questions

#### Why can't I open my home service from mobile Internet?

Possible causes: no port forward, double NAT, CGNAT, a firewall drop, the service listening on the wrong address.
