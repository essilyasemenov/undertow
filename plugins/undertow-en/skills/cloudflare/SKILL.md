---
name: cloudflare
description: "Cloudflare for publishing and protecting services: edge network, Anycast, CDN, reverse proxy, Proxied (orange cloud) and DNS only (grey cloud), DNS records and DNSSEC, SSL/TLS modes (Flexible, Full, Full strict, Automatic), edge certificates and Origin CA, supported proxy ports, WebSocket, gRPC, CF-Connecting-IP, WAF, rate limiting, DDoS, Cloudflare Tunnel (cloudflared), Zero Trust, Access, Cloudflare One Client (WARP), service tokens. Use when a domain, Remnawave Panel, subscription page or Node transport is published through Cloudflare: whether VLESS, Reality, XHTTP, WebSocket or gRPC Xray transport can go through the orange cloud or Cloudflare CDN, which port to pick, 52x errors, choosing proxy status and SSL mode, hiding the origin IP. Also general questions not tied to a project: how the SSL/TLS modes (Flexible, Full, Full strict) differ, which one to choose, what errors 525 and 526 mean."
license: MIT
---
# cloudflare

How exactly Cloudflare sits between the client and the origin. Without this model it is easy to get DNS, SSL/TLS, Tunnel or Zero Trust wrong. Answer in English.

## The base model

- For web traffic Cloudflare works as a reverse proxy on its edge network, not as a "universal TCP/UDP proxy by default".
- Anycast makes a request land on the nearest or an available Cloudflare edge location.
- CDN, caching, WAF and some security features are available only where traffic actually passes through the Cloudflare edge.
- `Proxied` versus `DNS only` is not a cosmetic difference but a choice of how traffic flows.

## Key terms

- `Orange Cloud` / `Proxied`: Cloudflare accepts web traffic on its edge network and can cache it, filter it and hide the origin IP.
- `Grey Cloud` / `DNS only`: Cloudflare only answers with the DNS record, and the client goes straight to the origin.
- `Edge Network`: Cloudflare's global network of points of presence, where edge certificates, CDN and security features apply.
- `Origin`: your server or an intermediate reverse proxy, such as Nginx Proxy Manager, Caddy or Nginx in front of Remnawave Panel.

## Sections (`references/`)

| Task | File |
| --- | --- |
| Record types, proxy status, DNSSEC | [dns.md](references/dns.md) |
| SSL/TLS modes, edge certificates, Origin CA | [ssl-tls.md](references/ssl-tls.md) |
| Standard Proxy/CDN: cache, ports, WebSocket, gRPC, headers | [proxy-cdn.md](references/proxy-cdn.md) |
| `cloudflared`, public hostnames, private network through Tunnel | [tunnel.md](references/tunnel.md) |
| Access, identity, policies, Cloudflare One Client, service tokens | [zero-trust.md](references/zero-trust.md) |
| WAF, custom rules, rate limiting, DDoS | [security.md](references/security.md) |
| Cloudflare next to Remnawave Panel, Node, subscriptions and homelab | [remnawave-integration.md](references/remnawave-integration.md) |
| Official links for all sections | [sources.md](references/sources.md) |

## Workflow

1. First determine the type of service: public web service, verification record, mail, private resource, Tunnel or non-standard transport.
2. Then determine whether traffic should go through the Cloudflare edge or straight to the origin.
3. Only after that choose the DNS record type, proxy status and SSL/TLS mode.
4. If the task concerns a VPN, panel, API, self-hosted application or home network, do not assume that the standard Cloudflare proxy suits any protocol.

## Practical rules

- If the goal is CDN, WAF, hiding the origin IP and edge certificates, you need `Proxied` web traffic.
- If the goal is mail, domain verification, some SRV/MX/TXT scenarios or an unsupported transport, `DNS only` is usually needed.
- If you need access to a private resource without an inbound port, consider Tunnel first, then decide separately whether Zero Trust access is needed on top of it.
- If the Cloudflare documentation names a product limitation, do not replace it with an assumption that "it should usually work".

## What not to do

- Do not describe Cloudflare as a replacement for any VPN or any L4 proxy without checking the specific product.
- Do not promise CDN or WAF benefits for `DNS only` records.
- Do not confuse the origin certificate with the edge certificate.
- Do not invent orange-cloud behavior for protocols the documentation does not confirm.

## Related skills

- Networking theory (DNS, TLS, CDN, anycast, reverse proxy): skill `network`.
- Remnawave settings (Hosts, Config Profiles, Xray transports): skill `remnawave`. This skill covers only the Cloudflare side.
- Choosing a topology (direct, cascade, CDN) under blocking: skill `architecture`.
- If publishing through Cloudflare affects how visible the VPN infrastructure is, run skill `detection-audit` before the final decision.
