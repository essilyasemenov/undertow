# IPv6

Use this section when you need to explain modern Internet addressing, dual-stack, global addresses, SLAAC, link-local and the role of ICMPv6.

## Simple explanation

IPv6 is the new version of IP with a much larger address space. It was created not only for more addresses but also for a more modern delivery model.

## Technical explanation

IPv6 is defined in RFC 8200. An address is 128 bits long. IPv6 makes heavy use of prefix-based routing, neighbor interaction through NDP and SLAAC automatic addressing, and depends critically on ICMPv6 for many mechanisms to work correctly, including PMTUD.

## History

- Created as a response to the limitations of IPv4.
- RFC 8200 replaced the earlier RFC 2460 specification.
- Unlike IPv4, IPv6 was designed from the start for a huge address capacity and a stricter fragmentation model.

## IPv6 in detail

### RFCs and normative basis

- RFC 4291 - IPv6 Addressing Architecture
- RFC 4443 - ICMPv6
- RFC 4861 - Neighbor Discovery for IPv6
- RFC 4862 - Stateless Address Autoconfiguration
- RFC 4193 - Unique Local IPv6 Unicast Addresses
- RFC 8200 - IPv6
- RFC 8201 - PMTUD for IPv6
- RFC 8504 - IPv6 Node Requirements

### Address types

| Type | Example | Purpose |
| --- | --- | --- |
| Global Unicast | `2001:db8::1` | Global routing |
| Link-local | `fe80::1` | Local service connectivity |
| Unique Local (ULA) | `fc00::/7`; in practice `fd00::/8` (locally assigned prefixes) | Local routing |
| Multicast | `ff02::1` | Group delivery |

### ASCII diagram

```text
host
  -> receives RA
  -> builds SLAAC address
  -> learns default router via link-local
  -> sends traffic using IPv6 routing
```

### Linux commands

```sh
ip -6 addr
ip -6 route
ip -6 neigh
ping6 2606:4700:4700::1111
traceroute6 2606:4700:4700::1111
tcpdump -ni any 'icmp6'
```

### Practical diagnostic examples

#### Checking the Router Advertisement and the default route

Check that there is a global address, a link-local next hop and a `::/0` route.

#### Checking ICMPv6 `Packet Too Big`

If some connections hang, look for filtering of critical ICMPv6 messages.

### Real network scenarios

#### Scenario 1. Dual-stack with broken IPv6

If the client prefers AAAA and the IPv6 path is partly broken, the user sees "the site takes forever", even though the IPv4 path is healthy.

#### Scenario 2. A home provider hands out a /56

The router can hand out different /64s per VLAN or LAN segment without NAT66.

### Common mistakes

- Blocking ICMPv6 as "unnecessary noise".
- Trying to think in the IPv4 broadcast model.
- Treating NAT as a mandatory part of IPv6.
- Dismissing link-local addresses as service-only and unimportant.

### Diagnostic order

1. Check for GUA/ULA/link-local addresses.
2. Check `::/0` and the next hop.
3. Check NDP and ICMPv6.
4. Check MTU/PMTUD.
5. Compare the IPv4 and IPv6 paths separately.

### Cross-references

- MTU and PMTUD: `mtu.md`
- Gateway and routing: `gateway.md`, `routing.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| IPv6 | The 128-bit internetworking protocol | Scalable addressing and delivery | Uses large addresses, prefix routing and ICMPv6 mechanisms | A huge address space | Requires careful operation of ICMPv6/NDP | `2001:db8::10` | The provider hands out a /56 or /64 for a home network | The successor of IPv4 |
| SLAAC | Stateless Address Autoconfiguration | Give a host an address automatically | The host builds an address from router advertisements and the prefix | Convenient for clients | Requires correct RAs | A client got a global `/64` address | A laptop automatically gets IPv6 on Wi-Fi | Relies on IPv6 RA |
| NDP | Neighbor Discovery Protocol | Find neighbors and the router | Uses ICMPv6 for neighbor solicitation/advertisement | Replaces ARP in IPv6 | Depends on ICMPv6 | `fe80::` router advertisement | A host learns the router's link-local address | A basic IPv6 mechanism |
| Link-local | An address for the local link | Local service connectivity | Formed and valid only within one link | Present on every interface | Not routed globally | `fe80::1` | The next hop in the routing table uses `fe80::` | Needed for the next hop in IPv6 |

## Examples

### Example 1. Dual-stack

A host has both:

- IPv4: `192.0.2.10`
- IPv6: `2001:db8:1::10`

A service may prefer IPv6 if there is an AAAA record and the path is available.

### Example 2. A link-local gateway

In IPv6 the next hop is often the router's link-local address rather than a global address.

### Example 3. Breakage because of ICMPv6

If the firewall drops `Packet Too Big` and other needed ICMPv6 messages, some connections will degrade or hang even though addresses and routes are present.
