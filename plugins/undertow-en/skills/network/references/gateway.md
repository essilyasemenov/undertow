# Gateway

Use this section when you need to explain how a host gets beyond its own subnet and why a wrong default gateway breaks the Internet even with a correct IP address.

## Simple explanation

The default gateway is the address of the router to which the host sends packets for all networks that are not in its own subnet.

## Technical explanation

The host first determines whether the destination IP address is within its local prefix. If it is, the host finds the neighbor's MAC address and sends the frame directly. If not, it uses the default route and sends the frame to the gateway's MAC address.

## History

- The concept of a gateway has historically been closely tied to early IP routing.
- In Cisco training materials, the default route and the gateway of last resort are basic elements of practice.

## Default Gateway in detail

### RFCs and normative basis

- RFC 1122 - Host Requirements
- RFC 1812 - Router Requirements
- RFC 4861 - Neighbor Discovery for IPv6

### Basic principle

A host does not know all the networks of the world. For non-local addresses, it sends the packet to the default gateway.

### ASCII diagram

```text
host 192.168.1.10/24
  -> destination 8.8.8.8 not local
  -> send frame to gateway 192.168.1.1 MAC
  -> router forwards further
```

### Differences between terms

| Term | Meaning |
| --- | --- |
| Default gateway | The host's gateway for non-local networks |
| Next hop | The next node in a specific route |
| Default route | The route `0.0.0.0/0` or `::/0` |

### Linux commands

```sh
ip addr
ip route
ip route get 8.8.8.8
arp -an
ip neigh
ping -c 3 <gateway-ip>
```

### Practical diagnostic examples

#### A wrong gateway from DHCP

```sh
ip route
ping -c 3 <gateway-ip>
```

If the gateway is outside the host's subnet, traffic will not leave the LAN.

#### No IPv6 default route received

Check the Router Advertisement, `ip -6 route`, `ip -6 neigh`.

### Real network scenarios

#### Scenario 1. A home client sees neighbors but not the Internet

Usually local L2 is fine, and the default gateway was not received, is wrong or is unreachable.

#### Scenario 2. A server with two interfaces

A wrong default route sends replies out of the wrong interface, and the connection looks "flaky".

### Common mistakes

- Setting a gateway that is not in your own IPv4 subnet.
- Assuming that a successful `ping` to a neighbor tests the default route.
- Ignoring a separate check of the IPv6 default route.

### Diagnostic order

1. Check the interface address and prefix.
2. Check the default route.
3. Check ARP/NDP to the gateway.
4. Check that the gateway itself has a path further.
5. For multi-homed systems, check policy routing.

### Cross-references

- Route selection: `routing.md`
- IPv6 neighbors: `ipv6.md`

## Glossary

| Term | Definition | Purpose | How it works | Advantages | Drawbacks/limitations | Practical example | Real scenario | Relation |
| --- | --- | --- | --- | --- | --- | --- |
| Default gateway | The router for unknown networks | Give the host a way out of the subnet | The host sends non-local traffic to the gateway address | A simple model | One wrong address breaks reachability | `192.168.1.1` on a home PC | A client reaches the Internet through the home router | Related to routing |
| Gateway of last resort | The router-side equivalent of the default route | Deliver traffic to unknown networks | Used when there is no more specific route | Universality | May become a black hole | `0.0.0.0/0 via ...` | A border router sends traffic to the provider | A special case of a route |
| ARP/NDP to the gateway | Looking up the gateway's L2 address | Pass the frame to the router | The host first learns the gateway's MAC/L2 identifier | Makes L3 reachable over L2 | Breaks with VLAN/L2 problems | The gateway MAC in the ARP cache | A client cannot reach the Internet because of an ARP failure | The link between L2 and L3 |

## Examples

### Example 1. A wrong gateway from DHCP

The client got `192.168.1.50/24`, but the gateway is `192.168.2.1`. Local hosts work, the Internet does not.

### Example 2. Access to a local server without a gateway

If the server and the client are in the same subnet, they can talk directly without the gateway.

### Frequent question

#### Why can I ping a neighboring address even though the gateway is broken?

Because traffic within the same subnet goes directly, not through the default gateway.
