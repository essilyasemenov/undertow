# HTTPS

## 1. What it is

`HTTPS` is the encrypted version of `HTTP` that uses `TLS` to protect communication between the client and the server. MDN defines HTTPS as a secure HTTP connection for exchanging sensitive data.

## 2. Why it is needed

- to protect logins, tokens, cookies and panel and API traffic;
- to prevent content from being tampered with along the path;
- to give the browser a `secure context`;
- to reduce the risk of `MITM` and SSL stripping.

## 3. How it relates to VPN infrastructure

- panels, dashboards, subscription pages and admin interfaces are almost always accessed over the web;
- even if the VPN transport is not HTTP, management usually goes through a browser and an API;
- unencrypted HTTP for the admin or public web layer creates unnecessary risk of leaks and tampering.

## 4. How it relates to Cloudflare

- Cloudflare often acts as the HTTPS entry point in front of the origin;
- when publishing through Cloudflare, you need to understand the redirect chain and the split into edge and origin segments;
- a certificate at the edge does not by itself secure the segment to the origin.

## 5. How it relates to Remnawave

- the `Remnawave` panel, API and subscription page are accessed over the web;
- a reverse proxy (Caddy, Nginx, `Nginx Proxy Manager` and others) is responsible for actually publishing backend services over HTTPS.

## 6. Common mistakes

- leaving the panel on HTTP without encryption;
- setting up a redirect without understanding HSTS and the risk of the first request over HTTP;
- forgetting about mixed content;
- confusing "HTTPS at the edge" with "a secure origin";
- publishing the backend over HTTPS but not closing direct access to it.

## 7. Diagnostics

1. Check what happens on an `http://` request.
2. Check whether the `https://` address opens.
3. Check the certificate validity period and the name match.
4. Check mixed content and the redirect chain.
5. Check the chain `DNS -> TCP/443 -> TLS -> HTTP response`.

## 8. Practical examples

- Moving the Remnawave Panel domain from HTTP to HTTPS behind a reverse proxy.
- Publishing the `Remnawave` subscription page over HTTPS behind Cloudflare.
- Analyzing mixed content after moving the panel to HTTPS.
- Comparing direct access to the origin with access through the CDN / proxy chain.

## 9. Checklist

- Find out what exactly is being published: a panel, an API, a dashboard or a subscription page.
- Check the redirect from HTTP to HTTPS.
- Check for mixed content and resources loaded over HTTP.
- Separate TLS, DNS, reverse proxy and firewall problems.
- If needed, go to `tls.md` and `reverse-proxy.md`.

## Sources

- MDN HTTPS glossary: <https://developer.mozilla.org/en-US/docs/Glossary/HTTPS>
- MDN TLS: <https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Transport_Layer_Security>
- Cloudflare Learning Center: <https://www.cloudflare.com/learning/>
- RFC 9110 HTTP Semantics (the `https` scheme): <https://www.rfc-editor.org/info/rfc9110/>
- RFC 8446 TLS 1.3: <https://www.rfc-editor.org/info/rfc8446/>
