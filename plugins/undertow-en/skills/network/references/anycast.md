# Anycast

## 1. What it is

`Anycast` is an addressing and routing method in which incoming traffic is directed to one of several nodes announcing the same address. Cloudflare describes anycast as a way to deliver a request to the nearest or most suitable data center, taking its capacity and availability into account.

## 2. Why it is needed

- to reduce latency by being close to a point of presence (edge);
- to increase resilience to overload and failures;
- to distribute traffic across many points of presence;
- to improve delivery and DDoS resilience for public services.

## 3. How it relates to VPN infrastructure

- anycast is useful for public DNS, dashboards, subscription addresses and global publishing through the edge;
- it does not replace VPN tunnel routing, but strongly affects the availability of DNS and management web interfaces;
- understanding anycast matters where users and services are geographically distributed.

## 4. How it relates to Cloudflare

- Cloudflare uses anycast for DNS and for delivering traffic through the edge;
- Cloudflare notes that traffic may arrive at a different data center than intuitively expected: Internet routing and peering are complex;
- anycast helps distribute load and maintain availability.

## 5. How it relates to Remnawave

- the `Remnawave` panel and subscription page can be published through Cloudflare;
- when diagnosing DNS and web publishing, keep in mind that the client talks to the edge first, not directly to the origin.

## 6. Common mistakes

- assuming anycast always leads to the geographically nearest point of presence (POP);
- expecting a stable route and traceroute, as with a single origin on a unicast address;
- confusing anycast with application-level load balancing;
- diagnosing only the origin when the user actually lands on the edge.

## 7. Diagnostics

1. Check whether the service goes through an anycast edge.
2. Separate edge behavior from origin behavior.
3. Do not draw conclusions from IP geography alone.
4. Remember that the path depends on BGP and peering, not only on distance.
5. For DNS, look separately at the path to the resolver and its availability.

## 8. Practical examples

- Why `1.1.1.1` and Cloudflare DNS answer quickly from different regions.
- Why a subscription page behind Cloudflare may be served from a different point of presence than the administrator expects.
- Why a traceroute to an anycast address does not match intuitive ideas about geography.
- How anycast helps survive DDoS and local data center failures.

## 9. Checklist

- Find out whether the address is anycast.
- Separate the location of the edge from the location of the origin.
- Do not merge anycast, CDN and load balancing into one concept.
- If needed, go to `bgp.md`, `cdn.md` and `dns-security.md`.

## Sources

- Cloudflare Anycast: <https://www.cloudflare.com/learning/cdn/glossary/anycast-network/>
- Cloudflare Anycast DNS: <https://www.cloudflare.com/learning/dns/what-is-anycast-dns/>
- Cloudflare Learning Center: <https://www.cloudflare.com/learning/>
