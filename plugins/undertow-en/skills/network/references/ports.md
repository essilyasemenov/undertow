# Ports

Use this section when you need to understand which service listens for a connection, why a process does not accept traffic, how the firewall and NAT rely on ports, and how well-known and ephemeral ports differ.

## Simple explanation

A port is a numeric identifier of an application within an IP host. IP delivers the packet to the machine, and the port helps deliver it to the right process.

## Technical explanation

Ports belong to the transport layer and are used by TCP and UDP. RFC 6335 sets the procedures for managing the registry of service names and transport ports. The same number can mean different things in TCP and UDP.

## History

- Ports appeared as a way to demultiplex network services on one host.
- As the Internet grew, a formal IANA registry and rules for managing it became necessary.

## Port ranges

| Range | Name | Typical purpose |
| --- | --- | --- |
| 0-1023 | Well-known | Core services, system protocols |
| 1024-49151 | Registered | Application services |
| 49152-65535 | Dynamic/Ephemeral | Temporary client ports |

## Ports and sockets in detail

### RFCs and normative basis

- RFC 6335 - Service Name and Transport Protocol Port Number Registry
- RFC 6056 - Recommendations for Transport Port Randomization

### Ephemeral ports in Linux

The ranges above are the IANA classification. By default Linux takes ephemeral client ports from `32768–60999`, not from `49152–65535`. The current range:

```bash
sysctl net.ipv4.ip_local_port_range
```

### Socket ASCII diagram

```text
client 192.168.1.10:53124/tcp
  -> server 93.184.216.34:443/tcp
```

### Linux commands

```sh
ss -lntup
lsof -i
nc -vz <host> <port>
tcpdump -ni any 'port 443'
nft list ruleset
```

### Practical diagnostic examples

#### Checking bind/listen

If a service listens only on `127.0.0.1:443`, it is unreachable from outside even if the firewall and routing are correct.

#### Checking a transport-specific port

`53/udp` and `53/tcp` are not the same thing. Check the needed protocol explicitly.

### Real network scenarios

#### Scenario 1. DNS does not always answer

Some queries go over UDP, while large answers require TCP/53 and break at the firewall.

#### Scenario 2. PAT at the border

The client's ephemeral ports become critical for NAT and conntrack: they are what distinguishes concurrent outgoing sessions.

### Common mistakes

- Checking only the port number without stating TCP/UDP.
- Treating "the port is open" as a guarantee that the application works.
- Ignoring the bind address.
- Forgetting about the client's ephemeral ports and NAT.

### Diagnostic order

1. Check whether the process listens on the needed IP:port/proto.
2. Check reachability of the port from the client.
3. Check the firewall/NAT rules.
4. Check the transport specifics (TCP or UDP) and capture traffic.

### Cross-references

- TCP and UDP: `tcp-vs-udp.md`
- NAT and PAT: `nat.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| Port | A numeric identifier of a transport endpoint | Deliver data to the right application | TCP/UDP use the port to demultiplex traffic | Demultiplexing services | Meaningless without a transport | `443/tcp` | A browser connects to a web server | Used by TCP and UDP |
| Well-known port | A port 0-1023 | Standardized core services | The number is assigned in advance to a common service | Predictability | Often requires privileges/is expected by policy | `22/tcp` | An SSH server listens on the standard port | Registered by IANA |
| Ephemeral port | A temporary client port | Create outgoing sessions | The OS temporarily allocates a free local port | Scalability of connections | Can be exhausted under load/NAT | `53124/tcp` | A browser opens dozens of connections to a CDN | Important for PAT/CGNAT |
| Socket | A local or remote transport endpoint | Connect a process to the network | A process does bind/listen or connect to an IP/port/proto combination | Precise addressing | The combination must be unique | `0.0.0.0:443` | A web server listens on all local addresses | Combines IP, port, proto |

## Examples

### Example 1. A client ephemeral port

The browser opens a connection:

```text
192.168.1.10:53124 -> 93.184.216.34:443/tcp
```

`53124` is the client's temporary port, `443` is the standard (well-known) service port on the server.

### Example 2. DNS and two transports

`53/udp` - ordinary short DNS queries.  
`53/tcp` - zone transfer, large answers, fallback.

### Example 3. Why `ss -lntup` beats guessing

The user says "nginx listens on 443". The check shows that the process actually listens only on `127.0.0.1:443`, so connections from outside are not established.
