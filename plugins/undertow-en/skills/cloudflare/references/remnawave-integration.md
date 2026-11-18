# Cloudflare next to Remnawave and homelab

How to fit Cloudflare into a VPN or homelab infrastructure on Remnawave. Recommendations stay strictly on the Cloudflare side, without invented settings for external systems.

## Scope of this section

- This section describes how Cloudflare behaves next to Remnawave Panel, the subscription page, Remnawave Node, `Nginx Proxy Manager` and home services.
- How to configure Hosts, Config Profiles and Xray transports themselves is the job of skill `remnawave`.
- If there is no confirmed Cloudflare-side setup for an external product, say so directly.
- Cloudflare architectural choices come first: `DNS only`, `Proxied`, `Tunnel`, `Access`, `Cloudflare One Client`, `Origin CA`, `WAF`.
- Basic terminology is in [SKILL.md](../SKILL.md), details are in the other `references/` files.

## Model

- Remnawave Panel and the subscription page are ordinary HTTP(S) services behind a reverse proxy at the origin; `Proxied`, Tunnel and Access apply to them.
- Remnawave Node accepts Xray client traffic. It cannot be assumed compatible with the standard Cloudflare proxy on any transport.
- A home network usually acts as the origin network or a private LAN behind Tunnel.
- `Nginx Proxy Manager` is a reverse proxy on the origin side, not a Cloudflare feature.
- If the transport is not confirmed HTTP/HTTPS traffic, first check whether `DNS only` or another Cloudflare product is needed.
- On the Cloudflare side, WebSocket and gRPC are confirmed with their requirements ([proxy-cdn.md](proxy-cdn.md)). These are Cloudflare's requirements for the traffic, not a guarantee that a particular Xray transport is compatible. Their ports differ: WebSocket can use any HTTPS port from the list (443, 2053, 2083, 2087, 2096, 8443), gRPC only 443.
- Do not describe `XHTTP` as guaranteed to work with the standard Cloudflare proxy: the Cloudflare documentation sets the limits of the HTTP/HTTPS proxy but does not confirm XHTTP specifically. Do not recommend `Proxied` as a ready-made XHTTP setting without confirmation for the specific setup.
- A `Proxied` name terminates TLS at the Cloudflare edge with Cloudflare's own certificate. Inference (not Cloudflare documentation text): a transport that needs its own TLS handshake between client and Node, such as `Reality`, will not pass through the standard Cloudflare proxy; such a name is `DNS only`.

## Workflow

1. Pin down the service: panel, subscription address, internal dashboard, API, private application or Node transport.
2. Determine whether it is web traffic or not.
3. Choose the publishing model: `Proxied` for supported web scenarios; `DNS only` for direct connections and transports the standard proxy does not support; `Tunnel` for secure publishing without exposing the origin IP; `Access` / `Cloudflare One Client` for private or admin-only access.
4. Choose the SSL/TLS mode and the origin certificate separately.
5. To protect the origin, consider allowing inbound traffic only from Cloudflare IPs, Authenticated Origin Pulls or Tunnel.

## Practical integration rules

- For `Nginx Proxy Manager`, Caddy or Nginx, describe Cloudflare as the external entry point (edge) and the reverse proxy as the origin.
- For Remnawave Panel, consider Tunnel + Access first rather than direct publishing: it is an admin interface.
- The subscription page is opened by client apps, not only by a browser. Access login and challenge rules are designed for a browser, so on this path they can break subscription updates (inference from the limitations in [security.md](security.md)).
- For a home network, first decide whether a public hostname or private access is needed.
- For Remnawave Node, do not claim that any inbound or transport can go through the orange cloud.
- If a name points to another CDN or proxy provider, do not put the Cloudflare proxy in front of it without explicit compatibility: TLS errors, a routing loop or connection failures are possible. Leave such a record `DNS only` by default.

## Infrastructure visibility

Publishing through Cloudflare changes which IP the client sees when connecting to the Node, but does not change the address the Node uses to reach websites. How this affects detection signals is the job of skill `detection-audit`.

## What not to do

- Do not invent compatibility of a non-standard VPN transport with the standard Cloudflare proxy.
- Do not present steps for NPM or Remnawave as "official Cloudflare steps".
- Do not turn Cloudflare into a universal answer to L4/L7 tasks without checking the product and the transport.
