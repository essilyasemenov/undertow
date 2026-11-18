# TLS

## 1. What it is

`TLS` is a protocol for secure communication between a client and a server over an untrusted network. MDN and Cloudflare describe TLS as a mechanism that provides encryption, integrity and authentication. On the web, TLS most often serves as the basis of `HTTPS`.

## 2. Why it is needed

- to protect traffic from being read or tampered with;
- to prove the server's identity with a certificate;
- to publish panels, APIs and subscription addresses securely;
- to reduce the risk of `MITM`, protocol version downgrade and stripping.

## 3. How it relates to VPN infrastructure

- VPN panels and management interfaces are usually published over TLS;
- even if the VPN transport itself is not HTTP, there is almost always a web interface or API next to it;
- delivering tokens, logins, configurations and panel sessions without TLS creates unnecessary risk.

## 4. How it relates to Cloudflare

- Cloudflare uses TLS at the edge and separately requires understanding TLS on the origin side;
- when publishing a panel through Cloudflare, you need to distinguish the "browser — Cloudflare" segment from the "Cloudflare — origin" segment;
- a certificate at the edge does not remove the need to protect the origin.

## 5. How it relates to Remnawave

- `Remnawave` publishes the panel and the API as web services;
- a reverse proxy (for example, Caddy, Nginx or `Nginx Proxy Manager`) usually terminates TLS in front of the backend services;
- TLS errors more often break management (panel, API, subscriptions) than the VPN tunnel itself.

## 6. Common mistakes

- using outdated TLS versions;
- confusing the certificate with the TLS protocol itself;
- assuming that the lock icon in the browser means a secure origin;
- terminating TLS at one layer and not taking into account that traffic is open further on to the backend;
- reducing DNS, TCP, TLS and HTTP to one cause of failure.

## 7. Diagnostics

1. Check DNS and IP reachability.
2. Check whether a TCP connection to `443` opens.
3. Check the certificate validity period and the name match.
4. Determine where TLS is terminated.
5. Check whether the firewall, MTU or the reverse proxy / CDN layer breaks the path.

## 8. Practical examples

- Publishing Remnawave Panel behind a reverse proxy with valid TLS.
- Protecting the `Remnawave` panel and API with TLS before publishing them to the Internet.
- Analyzing a case where the host is reachable by IP and route, but the HTTPS TLS handshake hangs.
- Explaining why a subscription page behind Cloudflare requires correct TLS on the origin.

## 9. Checklist

- Find out whether the question is about TLS as transport protection or about HTTPS publishing as a whole.
- Determine the path segments: client → CDN → reverse proxy → origin.
- Check the TLS versions and where TLS is terminated.
- Do not mix the certificate, DNS, the HTTPS redirect and the firewall policy.
- For web publishing, go to `https.md` and `reverse-proxy.md` if needed.

## Sources

- MDN TLS: <https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Transport_Layer_Security>
- MDN HTTPS glossary: <https://developer.mozilla.org/en-US/docs/Glossary/HTTPS>
- Cloudflare Learning Center: <https://www.cloudflare.com/learning/>
- Cloudflare TLS: <https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/>
- RFC 8446 TLS 1.3: <https://www.rfc-editor.org/info/rfc8446/>
