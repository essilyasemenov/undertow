# CDN

## 1. What it is

A `CDN` is a distributed network of edge servers that caches content closer to the user and helps deliver it faster, more reliably and more securely. Cloudflare describes a CDN as a way to speed up delivery, reduce latency and increase availability.

## 2. Why it is needed

- to shorten the physical distance to the user;
- to cache static resources and reduce load on the origin;
- to increase availability through distributed infrastructure;
- to add protection at the edge: certificate management and DDoS mitigation.

## 3. How it relates to VPN infrastructure

- a CDN is useful for management web interfaces, subscription pages and documentation portals;
- it does not replace the VPN transport itself, but hardens and speeds up the web infrastructure around it;
- when publishing panels and pages, you need to understand the difference between the path through the edge and the path to the origin.

## 4. How it relates to Cloudflare

- Cloudflare is the typical CDN and edge layer in this ecosystem;
- it adds caching, reliability, certificate handling and traffic filtering;
- it is important to distinguish a response from the edge from the real state of the origin.

## 5. How it relates to Remnawave

- the `Remnawave` panel and subscription page can be published through Cloudflare;
- in such a setup the reverse proxy (Caddy, Nginx, `Nginx Proxy Manager`) sits on the origin side behind the CDN;
- a CDN is especially useful for static web resources and public pages.

## 6. Common mistakes

- treating a CDN as a replacement for origin protection;
- forgetting that the CDN edge may cache responses and change the observed behavior;
- diagnosing only the origin IP when the client actually goes to the edge;
- proxying everything through the CDN without understanding which protocols it supports.

## 7. Diagnostics

1. Determine whether the request goes to the CDN edge or straight to the origin.
2. Understand what breaks: DNS, edge, origin, reverse proxy or the application.
3. Check caching and data freshness requirements.
4. Distinguish speed problems from availability or security problems.
5. Check the boundary between edge and origin.

## 8. Practical examples

- Publishing the `Remnawave` subscription page through the Cloudflare CDN.
- Analyzing why the panel's static resources load quickly while the API on the origin is slow.
- Comparing a direct origin response with a Cloudflare edge response.
- Explaining why anycast at the edge makes latency and traceroute hard to interpret.

## 9. Checklist

- Find out whether a CDN is used, and which one.
- Separate the "browser → edge" and "edge → origin" segments.
- Check whether the response should be cached.
- Do not confuse CDN, reverse proxy and WAF.
- If needed, go to `reverse-proxy.md`, `https.md` and `tls.md`.

## Sources

- Cloudflare Learning Center: <https://www.cloudflare.com/learning/>
- Cloudflare CDN: <https://www.cloudflare.com/learning/cdn/what-is-a-cdn/>
- Cloudflare TLS: <https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/>
