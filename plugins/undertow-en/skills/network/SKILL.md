---
name: network
description: "Networking fundamentals: OSI, TCP/IP, TCP and UDP, MTU/MSS, NAT/CGNAT, routing, gateway, DNS and DNS security (DoH/DoT/DNSSEC), IPv4/IPv6, ports, TLS/mTLS, HTTPS, HTTP/2/HTTP/3/QUIC, CDN, anycast, BGP, reverse proxy, load balancing, firewall, Linux networking. Use to explain networking concepts, diagnose connectivity, analyze routes, DNS, NAT, MTU and TLS problems, publish services behind a reverse proxy/CDN and choose a transport, including for Remnawave Panel and Node. Also Docker and the firewall: published container ports, ufw and iptables, why a container port is reachable from outside even though ufw blocks it."
license: MIT
---
# network

The common entry point for networking: core theory, applied diagnostics and connectivity design. It is the base layer for the other `undertow` skills: `remnawave`, `cloudflare`, `architecture` and `detection-audit` rely on it.

## How to work with this skill

1. Determine the class of problem: theory, diagnostics, design, publishing a service, performance degradation.
2. If the problem is not localized, start with [references/osi-model.md](references/osi-model.md).
3. If the real Internet stack model is needed, go to [references/tcp-ip.md](references/tcp-ip.md).
4. For addressing and connectivity, use the IPv4, IPv6, routing and gateway sections.
5. For application problems, check DNS, TCP/UDP, ports, NAT/CGNAT and MTU.
6. For secure publishing of services, VPN panels and edge infrastructure, use TLS, HTTPS, CDN, reverse proxy, firewall and linux-networking.
7. Read only the topic file you need from `references/`, not all of them.

## Topics (`references/`)

| Topic | File | When to open |
| --- | --- | --- |
| OSI | [osi-model.md](references/osi-model.md) | breaking a problem down by layer |
| TCP/IP | [tcp-ip.md](references/tcp-ip.md) | the practical Internet stack |
| TCP vs UDP | [tcp-vs-udp.md](references/tcp-vs-udp.md) | choosing a transport |
| MTU | [mtu.md](references/mtu.md) | MTU, MSS, PMTUD, fragmentation |
| NAT | [nat.md](references/nat.md) | address and port translation |
| CGNAT | [cgnat.md](references/cgnat.md) | carrier-grade NAT |
| Routing | [routing.md](references/routing.md) | path selection and routes |
| Gateway | [gateway.md](references/gateway.md) | the default gateway |
| DNS | [dns.md](references/dns.md) | name resolution |
| DNS security | [dns-security.md](references/dns-security.md) | DNSSEC, DoH, DoT, privacy |
| IPv4 | [ipv4.md](references/ipv4.md) | IPv4 addressing |
| IPv6 | [ipv6.md](references/ipv6.md) | IPv6 addressing, ICMPv6 |
| Ports | [ports.md](references/ports.md) | transport ports and sockets |
| TLS | [tls.md](references/tls.md) | TLS, certificates, handshake |
| mTLS | [mtls.md](references/mtls.md) | mutual authentication |
| HTTPS | [https.md](references/https.md) | HTTPS, redirects, secure publishing |
| HTTP/2, HTTP/3 | [http2-http3.md](references/http2-http3.md) | multiplexing, QUIC, head-of-line blocking |
| CDN | [cdn.md](references/cdn.md) | edge caching, origin shielding |
| Anycast | [anycast.md](references/anycast.md) | choosing the nearest edge |
| BGP | [bgp.md](references/bgp.md) | AS, path selection, inter-domain routing |
| Reverse proxy | [reverse-proxy.md](references/reverse-proxy.md) | upstream routing, publishing services |
| Load balancing | [load-balancing.md](references/load-balancing.md) | traffic distribution, failover |
| Firewall | [firewall.md](references/firewall.md) | filtering and exposure policy |
| Linux networking | [linux-networking.md](references/linux-networking.md) | interfaces, routes, sockets, link state |
| Sources | [sources.md](references/sources.md) | canonical RFCs and official documentation |

## Diagnostic order

```text
link
  -> L2 adjacency
    -> IP address/prefix
      -> route/default gateway
        -> DNS
          -> TCP/UDP and port
            -> NAT/CGNAT
              -> MTU/MSS/PMTUD
                -> application behavior
```

## Quality rules

- Prefer explaining from simple to technical without losing meaning.
- For normative statements, rely on RFCs.
- In practical examples, state the protocol, address family, port and traffic direction explicitly.
- Do not treat a working `ping` as proof that DNS, TCP, TLS or the application works.
- For a deep topic, go to the dedicated file instead of expanding the answer into an encyclopedic retelling.

## Related skills

- Remnawave product steps (install, nodes, subscriptions): skill `remnawave`.
- DNS, proxy/CDN, TLS modes and Tunnel on the Cloudflare side: skill `cloudflare`.
- Choosing a topology (direct, cascade, CDN) under blocking: skill `architecture`.
- If a conclusion affects how visible the VPN infrastructure is (GeoIP/ASN, DNS, routes, MTU), run skill `detection-audit` before the final decision.
