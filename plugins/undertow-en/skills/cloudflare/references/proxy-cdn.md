# Cloudflare Proxy CDN

Cloudflare's standard proxy and CDN for web traffic.

## Base model

- The terms `Proxied`, `DNS only`, edge and origin are defined in [SKILL.md](../SKILL.md); this file covers the behavior of the standard Cloudflare proxy once a name is `Proxied`.
- The standard Cloudflare proxy works for HTTP/HTTPS, not for arbitrary TCP/UDP traffic.
- Caching, WAF and some performance and security features apply only when the name is actually `Proxied`.
- The origin must understand that behind Cloudflare there may be the real client IP and a chain of proxy headers.

## What to check first

1. The proxy status of the name.
2. Whether the standard proxy supports this port.
3. Whether caching is needed at all or a bypass is required.
4. Whether WebSocket or gRPC is used and enabled in the zone settings.
5. How the origin recovers the real client IP.

## Supported ports

By default Cloudflare proxies only these ports:

| Protocol | Ports |
| --- | --- |
| HTTP | 80, 8080, 8880, 2052, 2082, 2086, 2095 |
| HTTPS | 443, 2053, 2083, 2087, 2096, 8443 |

- Caching is disabled on ports 2052, 2053, 2082, 2083, 2086, 2087, 2095, 2096, 8880 and 8443; it can be enabled only on Enterprise through a cache rule.
- For any other port there are two options: make the hostname `DNS only` or use Spectrum. Spectrum for all TCP/UDP ports is available only on Enterprise.
- On non-proxied ports the edge may accept the TCP connection, but HTTP/HTTPS requests will not reach the origin.

## WebSocket and gRPC

- WebSocket is enabled on the zone's **Network** page (the **WebSockets** toggle) or through the `websockets` API setting.
- gRPC is enabled in the same place (the **gRPC** toggle). Cloudflare's requirements:
  - the endpoint listens on port 443;
  - it supports TLS and HTTP/2, with HTTP/2 advertised through ALPN;
  - the request `Content-Type` is `application/grpc` or `application/grpc+<type>`;
  - the hostname is `Proxied`, and the SSL/TLS mode is at least `Full`.
- Through Cloudflare Tunnel, gRPC is supported only with private subnet routing, not through a public hostname.

## Origin-side headers

- `CF-Connecting-IP` is the preferred header for getting the original client IP at the origin.
- `X-Forwarded-For` is a chain of IP addresses through proxies, not one stable address.
- `X-Forwarded-Proto` shows which protocol the client used to reach Cloudflare.

## Practical rules

- If the application does auditing, rate limiting or access control by IP, first determine which header it should read.
- For origin logs, `CF-Connecting-IP` is usually more useful than parsing the `X-Forwarded-For` chain.
- For WebSocket, check that the application really works over WebSocket and fits within the web traffic Cloudflare supports.
- If the service listens on a non-standard port, check it against the port list above first.

## Caching

- Do not assume the Cloudflare cache is enabled and useful "by default for everything".
- Keep CDN, cache rules and availability through the reverse proxy as separate concerns.
- If data freshness or API behavior matters, first check whether a cache bypass or separate rules are needed.

## What not to do

- Do not describe the Cloudflare proxy as a replacement for a TCP load balancer.
- Do not replace `CF-Connecting-IP` with ad-hoc parsing of `X-Forwarded-For` when the task is to get the original client IP.
- Do not promise caching on any port or for any protocol.
