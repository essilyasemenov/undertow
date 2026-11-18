# Cloudflare SSL/TLS

The encryption mode between the client, the Cloudflare edge and the origin.

## Base model

- The edge certificate is the certificate Cloudflare presents to the visitor.
- The origin certificate is the certificate the origin presents to Cloudflare.
- The SSL/TLS mode defines how Cloudflare connects to the origin, not only what the user's browser sees.

## SSL/TLS modes

- `Automatic SSL/TLS`: the default mode. Cloudflare picks the most secure mode the origin can handle and moves traffic to it gradually (starting at 1%, then in 10% steps), rolling back on errors. It does not downgrade to a less secure mode on its own: if the origin certificate expires, `Full (strict)` stays, and you have to watch the certificate yourself.
- `Off`: HTTPS is not used.
- `Flexible`: HTTPS only between the client and Cloudflare; from Cloudflare to the origin traffic goes over HTTP. Use with great care and do not recommend it as the target configuration.
- `Full`: HTTPS between Cloudflare and the origin exists, but the origin certificate is not validated at all: it may be self-signed, expired or have a CN/SAN that does not match the hostname. The origin must accept HTTPS on port 443 and present some certificate, otherwise error `525`.
- `Full (strict)`: like `Full`, but the origin certificate must be unexpired, issued by a public CA or Cloudflare Origin CA, and contain a CN or SAN matching the requested hostname. Otherwise error `526`.
- `Strict (SSL-Only Origin Pull)`: Enterprise only. Cloudflare always uses TLS to the origin, regardless of the visitor's request scheme; the certificate is validated as in `Full (strict)`.

The mode can be overridden for some requests through Configuration Rules (API values: `off`, `flexible`, `full`, `strict`, `origin_pull`).

## Preferred approach

- Recommend `Full (strict)` by default.
- For the origin, use Cloudflare Origin CA or a valid public certificate.
- If the origin is Nginx Proxy Manager, Caddy or Nginx in front of Remnawave Panel, treat it as an ordinary origin-side reverse proxy: Cloudflare terminates the external TLS connection at the edge, and the reverse proxy accepts the connection from Cloudflare as the chosen mode requires.

## Edge certificates

- `Universal SSL` provides automatic Cloudflare edge certificates for activated domains.
- Keep in mind the coverage limits of Universal SSL, especially for second-level and deeper subdomains.
- If you need additional names, a choice of CA or other edge certificate parameters, the Advanced Certificate Manager and Custom certificates documentation describes them.

## Origin certificates

- `Cloudflare Origin CA` is intended only for the connection from Cloudflare to the origin.
- Do not describe Origin CA as a certificate for direct client connections that bypass Cloudflare.
- If the record is `DNS only`, the client goes straight to the origin, so the certificate must be trusted by the client itself, not only by Cloudflare.
- A public certificate (for example, Let's Encrypt) behind a `Proxied` hostname: the HTTP-01 challenge is blocked by `Always Use HTTPS` (it also redirects the `/.well-known/acme-challenge/*` path; use a redirect rule that excludes this path instead) and by Cloudflare Access on that hostname (the challenge request lands on the Access login). For an origin behind Access, DNS-01 or Cloudflare Origin CA is more reliable.

## Workflow

1. Determine whether traffic goes through a `Proxied` name or directly.
2. Determine who terminates TLS at the origin: the application itself, Nginx, Caddy, Nginx Proxy Manager or another reverse proxy.
3. Choose the SSL/TLS mode.
4. Check separately whether the edge certificate covers the needed name and whether the origin certificate is valid.
5. If the origin needs stronger protection, consider Authenticated Origin Pulls as an additional layer.

## What not to do

- Do not recommend `Flexible` as a long-term secure setup.
- Do not confuse Universal SSL with the origin certificate.
- Do not treat Origin CA as a valid answer for direct `DNS only` visitor access.
- Do not invent Nginx Proxy Manager toggle names that are not in the documentation.
- Do not count on `Automatic SSL/TLS` to save you from an expired origin certificate.
