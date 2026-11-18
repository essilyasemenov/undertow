# TCP/IP

Use this section when you need to explain how the Internet works in practice, without the excess abstraction of OSI.

## Simple explanation

TCP/IP is the family of protocols the Internet actually runs on. IP is responsible for addressing and delivering packets between networks, and TCP and UDP for passing data to applications.

## Technical explanation

The TCP/IP stack is usually seen as a 4-layer model: Link, Internet, Transport and Application. Encapsulation goes top-down, and routers make decisions mostly at the Internet layer without parsing application data.

## History

- The origins are ARPANET and early Internet experiments.
- MDN notes that the history of the Internet begins in the 1960s and moves to public infrastructure in the 1980s.
- The current TCP specification is consolidated in RFC 9293, IPv6 in RFC 8200.

## Components

- Link: Ethernet, Wi-Fi
- Internet: IPv4, IPv6, ICMP
- Transport: TCP, UDP
- Application: DNS, HTTP, SMTP, SSH

## Encapsulation diagram

```text
HTTP request
  -> TCP segment
    -> IP packet
      -> Ethernet frame
```

## Common mistakes

- Equating TCP/IP with TCP alone. IP and TCP are not the same thing.
- Assuming IP guarantees delivery and ordering. IP does not do that.
- Ignoring the transport and application layers when the route works.

## Diagnostics

- Check the IP address and route
- Check reachability to the remote IP
- Check the needed transport protocol and port
- Check the application protocol

## Best practices

- Explain any problem as the chain `application -> transport -> IP -> link`.
- Distinguish addressing, routing and delivery reliability.
- For any service, pin down: which IP, which transport, which port, which return path.

## Sources

- Cloudflare: TCP/IP
- MDN: How does the Internet work?
- RFC 9293, RFC 791, RFC 8200

## TCP/IP in detail

### The role of this section

This section describes the real Internet protocol suite. The behavior of specific transport protocols, MTU and DNS is in separate sections to avoid duplicating details.

### RFCs and normative basis

- RFC 791 - IPv4
- RFC 792 - ICMP for IPv4
- RFC 1122 - Host Requirements
- RFC 1123 - Host Requirements for Internet applications
- RFC 8200 - IPv6
- RFC 9293 - TCP
- RFC 768 - UDP

### Stack architecture

| TCP/IP layer | Purpose | Examples |
| --- | --- | --- |
| Application | Application logic | DNS, HTTP, SSH |
| Transport | Delivery to the application | TCP, UDP |
| Internet | Inter-network delivery | IPv4, IPv6, ICMP |
| Link | Local delivery | Ethernet, Wi-Fi |

### Encapsulation ASCII diagram

```text
application payload
  -> TCP/UDP header
    -> IP header
      -> Ethernet/Wi-Fi frame
```

### Packet path ASCII diagram

```text
client
  -> local switch/ap
  -> router/default gateway
  -> upstream routers
  -> destination server
```

### Linux commands

```sh
ip addr
ip route
ip route get 1.1.1.1
ping -c 3 1.1.1.1
traceroute 1.1.1.1
ss -lntup
tcpdump -ni any host 1.1.1.1
curl -v https://example.com
dig example.com
```

### Practical diagnostic examples

#### Checking IP connectivity without DNS

```sh
ping -c 3 1.1.1.1
curl -vk --connect-timeout 5 https://1.1.1.1
```

#### Checking route selection

```sh
ip route get 8.8.8.8
ip -6 route get 2606:4700:4700::1111
```

### Real network scenarios

#### Scenario 1. The web works over IPv4 but not over IPv6

This is not "TCP/IP is broken in general" but a partial failure of the Internet layer for one address family.

#### Scenario 2. The VPN is up, but some applications cannot get out

You need to separate:

- the IP route through the tunnel;
- the DNS path;
- the application's TCP/UDP behavior;
- the MTU in the tunnel.

### Common mistakes in practice

- Confusing the TCP/IP stack with TCP alone.
- Treating IP as a reliable transport.
- Ignoring the difference between addressing, routing and the application.
- Trying to diagnose HTTP without checking the IP route and the transport.

### Diagnostic order

1. Check the IP addresses on the interfaces.
2. Check the routing table and the route lookup.
3. Check reachability to the IP without DNS.
4. Check the needed transport and port.
5. Check the application protocol.

### Cross-references

- The diagnostic model: `osi-model.md`
- Transport: `tcp-vs-udp.md`
- Address families: `ipv4.md`, `ipv6.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TCP/IP | The Internet protocol family | Provide compatible inter-network communication | Layered encapsulation and separation of functions | Practically universal | Requires coordination of several protocols | Web access from a browser | A client reaches a site through DNS, TCP and IP | Includes IP, TCP, UDP, DNS |
| IP | The inter-network addressing and delivery protocol | Forward a packet between networks | Source/destination addresses and routing | Scalability | No guarantees of ordering or delivery | A packet arrives through several routers | A packet goes through the home router to a CDN | The basis for TCP/UDP |
| TCP | A reliable transport | Ordered delivery to the application | Connection, ACK, retransmission | Reliability | Overhead and latency | HTTPS, SSH | Loading a page or an SSH session | Runs on top of IP |
| UDP | An unreliable datagram transport | Fast connectionless transfer | Sending datagrams without a handshake | Low latency | Loss and reordering | DNS, VoIP | A voice call or a DNS query | Runs on top of IP |

## Examples

### Scenario 1. Accessing a website

```text
browser
  -> DNS resolves the IP
  -> TCP establishes a connection to 443/tcp
  -> IP delivers packets through routers
  -> HTTP/TLS exchange application data
```

### Scenario 2. Why ping does not equal "the site works"

- `ping` checks IP reachability, not HTTP.
- The site may fail to open because of DNS, TCP/443, TLS, the reverse proxy or the application.

### Common commands

```sh
ping 1.1.1.1
traceroute 1.1.1.1
ss -tn state established
curl -I https://example.com
dig example.com
```

### A common real case

The user says: "the VPN is connected, but the site does not load".

Analysis:

- The IP tunnel may be up.
- The TCP route back may be broken.
- DNS may not be going through the intended resolver.
- The MTU may be cutting large TCP segments.
