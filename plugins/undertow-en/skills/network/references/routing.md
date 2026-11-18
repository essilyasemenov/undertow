# Routing

Use this section when you need to understand how a packet chooses its path, why traffic goes the wrong way, how the default route works and how static routing differs from dynamic routing.

## Simple explanation

Routing is choosing the next step for a packet on its way to the destination network.

## Technical explanation

A router matches the destination IP address against the routing table, picks the most specific prefix, and then the next hop or a directly connected interface. Static routes are configured by hand; dynamic routes are distributed by routing protocols and change when the topology changes.

## History

- Static routing appeared as the basic way to connect networks.
- As networks grew, dynamic protocols became necessary for scaling and convergence.
- In Cisco training courses, the static route and the default route are treated as the simplest forms of routing.

## Routing in detail

### RFCs and normative basis

- RFC 791 - IPv4 forwarding context
- RFC 1812 - Requirements for IP Version 4 Routers
- RFC 8200 - IPv6 forwarding context
- RFC 2328 - OSPFv2
- RFC 4271 - BGP-4

### How the decision is made

```text
packet arrives
  -> inspect destination IP
  -> longest prefix match
  -> choose next hop or connected interface
  -> decrement TTL/Hop Limit
  -> forward
```

### Static and dynamic routing

| Type | Pros | Cons | Where to use |
| --- | --- | --- | --- |
| Static | Simplicity, predictability | No automatic adaptation | Home, small office, stub network |
| Dynamic | Convergence, scaling | Complexity | Enterprise, ISP, multiple paths |

### ASCII diagram

```text
host A
  -> router R1
    -> router R2
      -> remote subnet
```

### Linux commands

```sh
ip route
ip -6 route
ip route get 8.8.8.8
ip rule
traceroute 8.8.8.8
tracepath 1.1.1.1
```

### Practical diagnostic examples

#### Checking the longest prefix match

```sh
ip route get 10.20.30.40
```

The command shows which route and which `via` the kernel actually chose.

#### Checking for asymmetry

Capture with `tcpdump` on both uplinks and see whether the request goes out through one interface and the reply comes back through another.

### Real network scenarios

#### Scenario 1. A site-to-site VPN to a branch

You need a static route to the remote prefix through the tunnel interface or the address of the other end of the tunnel.

#### Scenario 2. Two providers on an edge router

Without policy routing or correct metrics, some traffic may return through the other WAN and break the stateful firewall and NAT.

### Common mistakes

- Looking only at whether a route exists, not at a specific route lookup.
- Ignoring more specific prefixes.
- Forgetting about the return route.
- Confusing the default route with a route policy.

### Diagnostic order

1. Check the routing table.
2. Run `ip route get` for the specific destination.
3. Check the next hop and reachability of the neighboring router.
4. Check the return route.
5. With multi-WAN, check policy routing and asymmetry.

### Cross-references

- The default gateway: `gateway.md`
- IPv4/IPv6 addressing: `ipv4.md`, `ipv6.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| Routing table | The table of routes | Choose the path to a network | The device looks up the best prefix and the corresponding exit | A fast local decision | Requires correct entries | `ip route` | A Linux host chooses the path to the VPN and to the Internet | The basis of L3 |
| Next hop | The next delivery node | Specify who to pass the packet to | The packet is sent to a neighboring router, not the final host | Splits the path into steps | An error breaks delivery | `via 192.0.2.1` | An edge router sends traffic to the provider | Related to the gateway |
| Static route | A route set by hand | A predictable path | The administrator adds the entry explicitly | Simplicity | Does not adapt by itself | `10.0.0.0/24 via 192.168.1.1` | A branch is reachable through one known next hop | An alternative to dynamic routing |
| Dynamic routing | Automatic distribution of routes | Scalability | Routers exchange routing information and recompute the path | Convergence and adaptation | Harder to operate | OSPF/BGP in general | A corporate network with several links | Used in large networks |
| Longest prefix match | Choosing the most specific prefix | Resolve overlapping networks correctly | A longer prefix takes priority | Precise matching | Requires understanding CIDR | `/24` wins over `/16` | Traffic to the office subnet goes to the VPN, everything else to the Internet | The basis of route selection |

## Examples

### Example 1. A static route to a branch

```text
branch network: 10.20.30.0/24
next hop: 192.168.100.2
```

The route is added by hand on the border router. While the topology is stable, this is a simple and reliable option.

### Example 2. Default route

If a home router does not know about thousands of external networks, it uses one default route towards the provider.

### Example 3. Asymmetry

A packet goes out through one WAN, the reply comes back through another, and the stateful firewall/NAT breaks it.

### Common commands

```sh
ip route
ip route get 8.8.8.8
traceroute 8.8.8.8
```
