# HTTP/2, HTTP/3, QUIC

## 1. What it is

`HTTP/2` and `HTTP/3` are modern versions of HTTP. MDN notes that `HTTP/2` reduces latency and head-of-line blocking, and that `HTTP/3` runs over `QUIC` on `UDP` instead of `TCP`. `QUIC` is a transport protocol with stream multiplexing, designed for fast connection setup and low latency.

## 2. Why it is needed

- to reduce latency and speed up loading;
- to carry several streams in one connection (multiplexing);
- to reduce head-of-line blocking;
- to publish modern web applications more efficiently.

## 3. How it relates to VPN infrastructure

- panels, dashboards and subscription pages are usually published as modern web applications;
- `HTTP/2` and `HTTP/3` behavior affects how responsive the panel and the API are;
- the path over QUIC/UDP matters especially where a firewall or network policy treats UDP differently from TCP.

## 4. How it relates to Cloudflare

- Cloudflare serves modern web protocols at its edge;
- `HTTP/3` and `QUIC` are especially visible at the CDN and edge level;
- the speed of panels and pages behind Cloudflare may differ from direct access to the origin.

## 5. How it relates to Remnawave

- `Remnawave` has web interfaces (the panel, the subscription page) whose perceived speed depends on the HTTP version;
- `Nginx Proxy Manager` and `NGINX` publish HTTP services, and it is important to understand the differences between protocol versions.

## 6. Common mistakes

- treating `HTTP/3` as just "fast HTTPS" without understanding QUIC;
- not taking into account that `HTTP/3` runs over UDP;
- confusing an application performance problem with a transport problem;
- forgetting that a firewall policy for UDP can break the QUIC path.

## 7. Diagnostics

1. Check which HTTP version is actually used.
2. Separate the TCP/TLS path from the UDP/QUIC path.
3. Check the firewall and middleboxes for UDP.
4. Check whether there is a fallback to HTTP/2 or HTTP/1.1.
5. Take into account which protocol versions the CDN and reverse proxy support.

## 8. Practical examples

- Analyzing why the panel works over HTTP/2 while HTTP/3 is unstable.
- Explaining the latency difference between TCP/TLS and QUIC.
- Analyzing the speed difference when accessing through the Cloudflare edge.

## 9. Checklist

- Find out which level the question is about: the HTTP version, the QUIC transport or browser behavior.
- Check whether UDP is involved in the path.
- Do not confuse a TLS problem with a QUIC/HTTP/3 problem.
- If needed, go to `tls.md`, `https.md` and `firewall.md`.

## Sources

- MDN HTTP/2: <https://developer.mozilla.org/en-US/docs/Glossary/HTTP_2>
- MDN HTTP/3: <https://developer.mozilla.org/en-US/docs/Glossary/HTTP_3>
- MDN QUIC: <https://developer.mozilla.org/en-US/docs/Glossary/QUIC>
- MDN Evolution of HTTP: <https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Evolution_of_HTTP>
- RFC 9110 HTTP Semantics: <https://www.rfc-editor.org/info/rfc9110/>
- RFC 9113 HTTP/2: <https://www.rfc-editor.org/info/rfc9113/>
- RFC 9000 QUIC: <https://www.rfc-editor.org/info/rfc9000/>
- RFC 9114 HTTP/3: <https://www.rfc-editor.org/info/rfc9114/>
