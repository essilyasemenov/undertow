# Mutual TLS

## 1. What it is

`mTLS` (mutual TLS) is a mode in which not only does the server prove its identity to the client, but the client also presents a certificate to the server. MDN notes that client certificate authentication is rare on the web but is used in specialized scenarios.

## 2. Why it is needed

- to strengthen the protection of sensitive admin interfaces and APIs;
- to authenticate connections between services;
- to restrict access to management without relying only on a password or token;
- to build a stricter trust model.

## 3. How it relates to VPN infrastructure

- mTLS is useful for secure management, internal APIs and service-to-service traffic;
- it is relevant where the panel, agents or internal tools exchange sensitive data;
- mTLS is not the same as ordinary HTTPS: the server must trust the client's certificate.

## 4. How it relates to Cloudflare

- with Cloudflare you have to think separately about trust on the "browser — Cloudflare" segment and on the "Cloudflare or service — origin" segment;
- mTLS is especially useful for connections to the API on the origin and for sensitive admin paths;
- when publishing through Cloudflare, it is important to understand where mTLS applies at all: in the browser, at the edge or between services on the origin side.

## 5. How it relates to Remnawave

- Panel connects to the Node API (`NODE_PORT`) over mTLS: both sides present certificates issued by Remnawave's internal CA; the Node receives its keys and certificates in `SECRET_KEY` (details: skill `remnawave`);
- for `Nginx Proxy Manager`, mTLS is a separate advanced layer, not an ordinary HTTPS toggle.

## 6. Common mistakes

- confusing mTLS with ordinary TLS;
- expecting browser login to always work smoothly with client certificates;
- not separating public web publishing from authentication of internal services;
- forgetting that both sides must trust the certificate chain.

## 7. Diagnostics

1. Check whether a client certificate is required.
2. Check certificate trust on both sides.
3. Separate a general TLS failure from a client authentication failure.
4. Check on which segment of the path mTLS applies.
5. Do not mix HTTPS for the browser with mTLS between services.

## 8. Practical examples

- Protecting an internal admin interface or API behind a reverse proxy with a client certificate.
- Analyzing why an ordinary browser login does not get through to a route protected by mTLS.
- Explaining where mTLS fits for management and where ordinary HTTPS is enough.
- Interaction of internal components with client certificate authentication.

## 9. Checklist

- Find out whether public HTTPS or specifically mutual authentication is needed.
- Check who is the client and who is the server in the trust model.
- Do not confuse mTLS with "TLS just being enabled".
- If needed, go to `tls.md`, `https.md` and `reverse-proxy.md`.

## Sources

- MDN TLS: <https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Transport_Layer_Security>
- Cloudflare TLS: <https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/>
- NGINX documentation: <https://nginx.org/en/docs/>
- RFC 8446 TLS 1.3 (client certificate authentication): <https://www.rfc-editor.org/info/rfc8446/>
