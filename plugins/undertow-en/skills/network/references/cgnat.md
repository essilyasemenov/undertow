# CGNAT

Use this section when the user has Internet access but no public IPv4 of their own, and inbound connections, port forwarding or some P2P/VPN scenarios do not work.

## Simple explanation

CGNAT is NAT at the provider. The subscriber gets not a unique public IPv4 but an address from a shared pool or private space, and then shares one external address with other subscribers.

## Technical explanation

The operational side of CGNAT is standardized in RFC 6888. It is a large-scale carrier NAPT platform with big translation tables, logging and limits on ports/timeouts.

## History

- It spread widely because of public IPv4 exhaustion.
- It became a compromise between the need to keep IPv4 reachability and the high cost of public addresses.

## Main consequences

- no direct inbound IPv4 without special provider services;
- self-hosting is harder;
- log correlation is harder;
- there may be limits on the number of concurrent sessions/ports.

## CGNAT in detail

### RFCs and normative basis

- RFC 6598 - Shared Address Space `100.64.0.0/10`
- RFC 6888 - Common Requirements for Carrier-Grade NATs

### How to recognize CGNAT

- The router's WAN address does not match the external IP.
- The WAN gets an RFC 1918 address or one from `100.64.0.0/10`.
- Port forwarding on the home router does not give inbound reachability.

### ASCII diagram

```text
LAN host 192.168.1.10
  -> home NAT
100.64.10.5
  -> ISP CGNAT
198.51.100.25
  -> Internet
```

### Linux commands

```sh
ip addr
ip route
curl -4 ifconfig.me
traceroute 1.1.1.1
```

### Practical diagnostic examples

#### Comparing the WAN IP and the external IP

```sh
curl -4 ifconfig.me
```

If the external IP differs from the WAN address on the router, an intermediate NAT is very likely.

#### Checking an unreachable port forward

If the service inside the LAN is listening, local DNAT is configured, but it is unreachable from outside and the WAN is not public, it is typical CGNAT.

### Real network scenarios

#### Scenario 1. A home VPN server is unreachable from a mobile network

The cause may be not the WireGuard config but the lack of a public IPv4 of your own.

#### Scenario 2. Complaints about the reputation of the external IP

Dozens or hundreds of subscribers may live behind one IP, so blocklists and rate limits sometimes affect innocent users.

### Common mistakes

- Trying to fix CGNAT with an ordinary port forward on your own router.
- Confusing a private WAN address with a "static public" one.
- Looking for the cause only in the LAN server's firewall.

### Diagnostic order

1. Check the WAN IP.
2. Compare it with the external IP visible from the Internet.
3. Ask the provider whether CGNAT is used and whether a public IPv4 service is available.
4. If needed, switch to IPv6, a reverse tunnel or a VPS.

### Cross-references

- Basic NAT: `nat.md`
- IPv6 as an alternative to inbound IPv4: `ipv6.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| CGNAT | Carrier-scale provider NAT | Save public IPv4 addresses | The provider aggregates subscribers behind shared addresses and port pools | Scalability for the ISP | No full inbound IPv4 | Mobile operator | A home port forward does not work because of the provider's NAT | An extension of NAT |
| Shared IPv4 | A shared external IPv4 for several subscribers | Reduce address consumption | One external address is used by many clients through different ports | High utilization density | Harder logs and reputation | Several clients behind one IP | Complaints about shared IP reputation | Typical of CGNAT |
| Port quota | A limit on the number of ports/sessions | Control CGNAT resources | The provider allocates part of the port space to the subscriber | Predictable load | May break P2P/mass connections | A P2P client hits the limit | Many outgoing sessions from one subscriber | Part of CGNAT policy |

## Examples

### Example 1. Port forwarding does not work

The user configured `443 -> 192.168.1.20:443` on the home router, but the service is unreachable from outside. The router's WAN has `100.64.23.10`, and an external service shows `198.51.100.77`. This is a typical sign of CGNAT.

### Example 2. A VPN server at home

A home WireGuard server does not accept inbound packets from the Internet when CGNAT is present. Solutions:

- request a public IPv4;
- use IPv6;
- run the server on a VPS and build a tunnel to it.

### Frequent question

#### Why can websites work while inbound connections do not?

Because CGNAT passes outgoing connections through its translation tables, while an incoming connection for which no table entry exists has nowhere to be delivered.
