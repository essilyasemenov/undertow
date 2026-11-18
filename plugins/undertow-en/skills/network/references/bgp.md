# BGP

## 1. What it is

`BGP` (Border Gateway Protocol) is the main routing protocol between networks of different operators on the Internet. RFC 4271 defines BGP-4 as a protocol for exchanging routing information between autonomous systems.

## 2. Why it is needed

- to connect autonomous systems into a single Internet;
- to choose the path to remote networks;
- to maintain global reachability of CDNs, DNS, clouds and providers;
- to enable anycast publishing and edge infrastructure distributed across many networks.

## 3. How it relates to VPN infrastructure

- BGP indirectly determines how users reach the DNS, CDN, panels and public addresses around the VPN;
- global availability of `Remnawave`, subscription pages and publishing through Cloudflare depends on routing between operators;
- failures in Internet routing can look like "the panel is unreachable from one country or network".

## 4. How it relates to Cloudflare

- Cloudflare uses BGP together with anycast to direct traffic to the edge;
- anycast behavior depends directly on Internet routing and peering relationships;
- Cloudflare explicitly warns that traffic does not always go to the intuitively "nearest" data center.

## 5. How it relates to Remnawave

- availability of the `Remnawave` panel and API from different networks depends on stable Internet routing;
- understanding BGP helps explain regional degradation, different latency over different paths and edge anomalies.

## 6. Common mistakes

- thinking the Internet always picks the geographically shortest path;
- confusing BGP with internal static routing or OSPF;
- treating latency as the only factor in path selection;
- ignoring differences in peering and routing policies between operators.

## 7. Diagnostics

1. Check whether the problem is local or depends on the network and region.
2. Distinguish an origin or service failure from an Internet path anomaly.
3. Remember that traceroute shows the observed path, not the logic of routing policies.
4. Take anycast and CDN behavior into account.
5. For Internet-scale problems, look at BGP and external routing, not only at the host firewall.

## 8. Practical examples

- Why the Cloudflare edge answers quickly from one provider's network and more slowly from another's.
- Why anycast DNS leads different providers to different points of presence.
- Why a panel is reachable from one region and has problems from another with the same origin.
- Explaining why the data center "nearest on the map" is not necessarily the one chosen.

## 9. Checklist

- Find out whether the problem is local or depends on the path through the Internet.
- Do not mix BGP with the host routing table.
- Take anycast, CDN and peering into account.
- If needed, go to `anycast.md`, `cdn.md` and `routing.md`.

## Sources

- RFC 4271 BGP-4: <https://www.rfc-editor.org/info/rfc4271/>
- Cisco Networking Academy: <https://www.netacad.com/courses/ccna-switching-routing-wireless-essentials>
- Cloudflare Learning Center: <https://www.cloudflare.com/learning/>
- Cloudflare Anycast: <https://www.cloudflare.com/learning/cdn/glossary/anycast-network/>
