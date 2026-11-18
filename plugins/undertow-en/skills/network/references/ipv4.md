# IPv4

Use this section when you need to explain IPv4 addressing, private and public networks, subnets, broadcast and the reasons NAT became so widespread.

## Simple explanation

IPv4 is the 32-bit addressing system of the Internet. An address is written as four octets, for example `192.168.1.10`.

## Technical explanation

IPv4 is defined in RFC 791. Modern addressing is based on CIDR prefixes, not on the old classful model. The address space is limited, so public IPv4 addresses are scarce and are often compensated for with NAT.

## History

- IPv4 became the foundation of the early Internet.
- At first the address space seemed sufficient.
- The growth of the Internet led to an address shortage and mass use of RFC 1918 + NAT.

## IPv4 in detail

### RFCs and normative basis

- RFC 791 - IPv4
- RFC 919 - Broadcasting Internet Datagrams
- RFC 922 - Broadcasting Internet Datagrams in the Presence of Subnets
- RFC 1519 - CIDR strategy
- RFC 1918 - private addressing
- RFC 4632 - Classless Inter-domain Routing

### Address structure

```text
192.168.1.10/24
network   192.168.1.0
host      10
broadcast 192.168.1.255
```

### Private ranges

| Range | Purpose |
| --- | --- |
| 10.0.0.0/8 | Private |
| 172.16.0.0/12 | Private |
| 192.168.0.0/16 | Private |

### ASCII diagram

```text
host 192.168.1.10/24
  -> local 192.168.1.20 direct
  -> remote 8.8.8.8 via gateway 192.168.1.1
```

### Linux commands

```sh
ip addr
ip route
ipcalc 192.168.1.10/24
arp -an
ping -c 3 192.168.1.1
```

### Practical diagnostic examples

#### A wrong netmask

If a host considers a remote address local because the prefix is too wide, it will send ARP requests for what should go through the gateway.

#### Overlapping subnets with a VPN

Two sites use `192.168.1.0/24`, and route selection becomes ambiguous.

### Real network scenarios

#### Scenario 1. A home network and NAT

The client gets an RFC 1918 address via DHCP and reaches the Internet through NAT on the edge router.

#### Scenario 2. A site-to-site VPN between two offices

You cannot pick identical private prefixes without thinking, otherwise routing between the sites will conflict.

### Common mistakes

- Thinking in classful addressing instead of CIDR.
- Ignoring overlap of private networks.
- Confusing the broadcast address with the network address.
- Treating private IPv4 as suitable for direct publishing on the Internet.

### Diagnostic order

1. Check the address and prefix.
2. Check which address is considered local and which remote.
3. Check the default gateway and ARP.
4. Check overlap with the VPN and other networks.

### Cross-references

- NAT: `nat.md`
- Gateway and routing: `gateway.md`, `routing.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| IPv4 | The 32-bit internetworking protocol | Addressing and delivering packets | A packet carries the source/destination address and is forwarded by routers | Universal support | Limited address space | `203.0.113.10` | A home client reaches the Internet over IPv4 | The basis of most current networks |
| CIDR | The prefix-based addressing model | Divide the address space flexibly | The address space is described by the prefix length | Efficiency | Requires understanding prefixes | `/24`, `/27` | A VPN breaks because of overlapping prefixes | Used in routing |
| Broadcast | The address of all hosts in a subnet | Local broadcast tasks | A packet is delivered to all nodes of the segment/subnet | Simple discovery in the IPv4 L2/L3 model | Can be noisy in large networks | `192.168.1.255` | ARP and some legacy discovery mechanisms | An IPv4-specific feature |
| Private IPv4 | The non-public RFC 1918 ranges | Address internal networks | Used inside the network and not routed globally | Saves public addresses | Requires NAT for the Internet | `192.168.1.0/24` | A home router hands out private addresses via DHCP | Related to NAT |

## Examples

### Example 1. A home subnet

`192.168.1.0/24` is a local network where:

- gateway: `192.168.1.1`
- client: `192.168.1.10`
- broadcast: `192.168.1.255`

### Example 2. Conflicting address plans

Two sites use `192.168.1.0/24`. The site-to-site VPN comes up, but the routes conflict. This is a common operational mistake with private IPv4 addresses.

### Example 3. A public and a private address

A server inside the LAN has `10.0.0.5` and is seen from outside as `198.51.100.25` after NAT.
