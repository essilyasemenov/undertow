# TCP vs UDP

Use this section when you need to choose a transport protocol, explain how a service behaves, or understand why one flow is sensitive to loss and another to latency.

## Simple explanation

TCP makes delivery reliable and ordered. UDP makes delivery fast and simple, but without guarantees.

## Technical explanation

TCP is a connection-oriented transport: handshake, sequence numbers, acknowledgments, retransmission, flow control and congestion control. UDP is a connectionless datagram protocol with a minimal header and no built-in guarantees of delivery or ordering.

## History

- UDP is standardized in RFC 768.
- TCP was historically RFC 793, and the current consolidated specification is RFC 9293.
- The growth of real-time traffic made the TCP/UDP trade-off especially visible in VoIP, video streaming and DNS.

## Comparison

| Property | TCP | UDP |
| --- | --- | --- |
| Connection | Yes | No |
| Delivery order | Guaranteed | Not guaranteed |
| Resending lost data | Yes | No |
| Congestion control | Yes | Not at the protocol level |
| Startup latency | Higher | Lower |
| Typical scenarios | HTTPS, SSH, SMTP | DNS, VoIP, gaming, telemetry |

## Common misconceptions

- "UDP is better than TCP because it is faster": not always; for critical data, loss can make the application worse.
- "UDP has no ports": it does, RFC 768 defines the source and destination port.
- "TCP is always slower": on a healthy network TCP can be optimal thanks to reliability and flow control.

## Diagnostics

- TCP: look at the handshake, retransmissions, the window and resets (RST).
- UDP: look at whether the packet was sent and received, loss, jitter and application-level retries.

## TCP and UDP in detail

### RFCs and normative basis

- RFC 768 - UDP
- RFC 8085 - UDP Usage Guidelines
- RFC 9293 - TCP

### Comparison: details

| Property | TCP | UDP |
| --- | --- | --- |
| Type | Connection-oriented | Connectionless |
| Ordering guarantee | Yes | No |
| Resending lost data | Yes | No |
| Congestion control | Built in | At the application level or absent |
| Typical use | HTTPS, SSH, SMTP | DNS, VoIP, telemetry, media |

### TCP ASCII diagram

```text
client SYN
  -> server SYN-ACK
    -> client ACK
      -> data
        -> ACK/retransmission/window control
```

### UDP ASCII diagram

```text
client datagram
  -> network
    -> server datagram receive or loss
```

### Linux commands

```sh
ss -tn
ss -un
tcpdump -ni any 'tcp port 443'
tcpdump -ni any 'udp port 53'
nc -vz example.com 443
dig @1.1.1.1 example.com
```

### Practical diagnostic examples

#### TCP: the SYN goes out, no SYN-ACK comes back

```sh
tcpdump -ni any 'tcp[tcpflags] & (tcp-syn|tcp-ack) != 0 and host <server-ip>'
```

Possible causes:

- firewall;
- wrong DNAT;
- return route;
- the service is not listening.

#### UDP: the request went out, no answer

```sh
tcpdump -ni any 'udp and host <server-ip>'
dig @<server-ip> example.com
```

Possible causes:

- packet loss;
- fragmentation;
- ACL/firewall;
- the application does not answer.

### Real network scenarios

#### Scenario 1. DNS is unstable only over UDP

Small answers pass, large ones are cut because of MTU/firewall, and the TCP fallback saves some of the queries.

#### Scenario 2. Voice in a call breaks up while HTTPS works

UDP media traffic is sensitive to jitter and loss, while TCP web traffic compensates for loss with retransmissions.

### Common mistakes

- Calling UDP "broken TCP without a handshake".
- Assuming that no handshake means no ports and no state in the application.
- Expecting built-in reliability from UDP.
- Judging real-time traffic by throughput alone.

### Diagnostic order

1. Find out which transport the service uses.
2. Check the listening socket or that datagrams are generated.
3. Capture traffic and see the direction of the exchange.
4. For TCP, look for handshake problems, retransmissions and resets.
5. For UDP, look for loss, ACLs, MTU and application logs.

### Cross-references

- Ports and sockets: `ports.md`
- Packet size and PMTUD: `mtu.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| Handshake | The procedure for establishing a TCP connection | Agree on parameters and start a reliable exchange | Exchange of SYN, SYN-ACK, ACK | State control | Adds an RTT | HTTPS | Opening SSH or TLS | Part of TCP |
| Datagram | An independent UDP message | Send a unit of data quickly | Sent without establishing a connection | Simplicity | No built-in reliability | DNS query | A voice packet in VoIP | Part of UDP |
| Retransmission | Resending in TCP | Compensate for loss | Lost segments are sent again after a timer/ACK analysis | Reliability | May increase latency | A file download | Bad Wi-Fi, but the file still downloads | Depends on ACKs |
| Checksum | A checksum | Detect data corruption | The receiver checks the control value | Basic protection | Does not solve packet loss | UDP checksum | A DNS answer is dropped as corrupted | Present in TCP and UDP |

## Examples

### Example 1. DNS lookup

- The client sends a short UDP query to `53/udp`.
- If the answer is too large or a zone transfer is needed, TCP may be used.

### Example 2. A video call

Losing some packets is better than accumulating latency because of retransmissions. That is why media streams often run over UDP.

### Example 3. SSH

SSH requires a correct byte sequence and reliability. A lost byte breaks the session, so TCP fits better.

### Common commands

```sh
ss -tn
ss -un
tcpdump -ni any 'tcp port 22'
tcpdump -ni any 'udp port 53'
nc -vz example.com 443
dig example.com
```

### A typical incident

A monitoring service sends telemetry over UDP, and some events are lost when the WAN is overloaded. This is not "a broken server" by default; it may be the expected behavior of an unreliable transport under load.
