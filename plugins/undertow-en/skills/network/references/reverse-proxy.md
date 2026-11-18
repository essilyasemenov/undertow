# Reverse Proxy

## 1. What it is

A `Reverse proxy` accepts a client request, passes it to a server behind it (the upstream) and returns the response to the client. The official NGINX documentation describes this as the basic proxying configuration: passing requests, modifying request headers and controlling buffering.

## 2. Why it is needed

- to publish internal services through one external entry point;
- to hide the internal topology of the origin;
- to terminate TLS and configure redirects centrally;
- to route traffic to different internal services.

## 3. How it relates to VPN infrastructure

- VPN management interfaces are usually published through a reverse proxy;
- this applies to the panel web interface, subscription pages, APIs and dashboards;
- the reverse proxy becomes the boundary between the Internet and the internal services.

## 4. How it relates to Cloudflare

- when publishing through Cloudflare, the reverse proxy usually sits on the origin side;
- CDN and reverse proxy are different layers: delivery at the edge and request handling at the origin;
- errors most often occur at the junction `Cloudflare -> NGINX/NPM -> upstream`.

## 5. How it relates to Remnawave

- the `Remnawave` documentation requires publishing the panel only through a reverse proxy and lists the options: Caddy, Nginx, Traefik, Angie;
- the reverse proxy hides the backend ports (`127.0.0.1:3000`) and terminates HTTPS.

## 6. Common mistakes

- publishing the backend directly, bypassing the reverse proxy;
- confusing a reverse proxy with a CDN;
- breaking headers or the request scheme when passing to the upstream;
- forgetting that buffering and forwarding change application behavior;
- not understanding where TLS ends and unencrypted HTTP to the upstream begins.

## 7. Diagnostics

1. Check that the reverse proxy itself is reachable.
2. Check whether the upstream answers directly, without the proxy.
3. Check routing by host name and path.
4. Check headers and the scheme (`http`/`https`) between the layers.
5. Check whether the root cause is in DNS, the firewall or the CDN.

## 8. Practical examples

- Publishing the `Remnawave` panel behind `NGINX`.
- Analyzing `502/504` errors when the backend does not listen on the expected port.
- Comparing direct access to the backend with access through Cloudflare + reverse proxy.

## 9. Checklist

- Determine whether there is a chain `client -> CDN -> reverse proxy -> application`.
- Find out the scheme, port and host-name routing for the upstream.
- Do not reduce reverse proxy, TLS and firewall to one cause.
- For Nginx Proxy Manager, check whether the backend is open, bypassing the proxy.
- If needed, go to `https.md`, `tls.md` and `firewall.md`.

## Sources

- NGINX reverse proxy admin guide: <https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/>
- NGINX documentation: <https://nginx.org/en/docs/>
