# Firewall

## 1. What it is

A `Firewall` is a layer for filtering network traffic and enforcing access policies. On Linux hosts it is implemented through `nftables` (and front ends such as `ufw`) and controls access between interfaces, zones and services.

## 2. Why it is needed

- to reduce the attack surface;
- to allow only the needed inbound and outbound flows;
- to separate LAN, WAN and service zones;
- to prevent accidental publishing of panel, API and backend ports.

## 3. How it relates to VPN infrastructure

- an imprecise firewall policy breaks VPN infrastructure in terms of both security and availability;
- open admin ports, wrong forwards and overly broad allow rules create unnecessary risk;
- the firewall determines which management and data paths are actually reachable.

## 4. How it relates to Cloudflare

- Cloudflare does not replace the local firewall on the origin;
- even when publishing through the edge, the origin firewall must restrict direct access;
- the firewall is especially important if the origin IP is directly reachable.

## 5. How it relates to Remnawave

- the Remnawave docs require not publishing services directly: in the official `docker-compose` the Panel ports (`3000`, `3001`) and Postgres (`6767`) are bound to `127.0.0.1`;
- allow `NODE_PORT` on the Node only from the Panel IP;
- for `Nginx Proxy Manager` and other reverse proxies, the firewall ensures that the backend is reachable only through the proxy.

## 6. Docker and ufw

The Docker documentation warns that Docker and `ufw` are incompatible. Docker redirects traffic to published container ports (`ports:` in compose) in the `nat` table before it reaches the `INPUT` and `OUTPUT` chains that `ufw` uses. So a `ufw deny` rule does not close such a port.

- Publish a port that must not be reachable from outside on `127.0.0.1` (as in the official Remnawave compose), or do not publish it at all.
- Containers with `network_mode: host` (this is how Remnawave Node runs) do not use Docker port forwarding; their ports are filtered by the ordinary host firewall.

## 7. Common mistakes

- opening extra ports "just in case";
- treating a CDN or reverse proxy as a replacement for a firewall;
- allowing direct access to backend or panel ports;
- not distinguishing external publishing from access between nodes inside the network;
- changing the firewall without checking the return path of traffic;
- closing a container port with `ufw` and assuming it is closed.

## 8. Diagnostics

1. Determine which traffic must be allowed and between which zones.
2. Check whether the service is reachable locally and unreachable only from outside.
3. Check whether the origin is open, bypassing the proxy or CDN.
4. Look separately at the host firewall, the router firewall and filtering at the edge.
5. Check the expected path and the unwanted direct path.

## 9. Practical examples

- Restricting access to Remnawave Panel to the reverse proxy only.
- Restricting the `Remnawave` origin so that only the needed web entry point works publicly.
- Checking that the backend behind `Nginx Proxy Manager` does not accept direct connections from the Internet.

## 10. Checklist

- Determine where exactly the firewall sits: host, router, cloud edge.
- Check the expected path and the unwanted direct path.
- Separate a service exposure problem from an application problem.
- For Cloudflare and a reverse proxy, check separately whether the origin is directly reachable.
- If needed, go to `linux-networking.md` and `reverse-proxy.md`.

## Sources

- nftables wiki: <https://wiki.nftables.org/>
- Ubuntu UFW: <https://ubuntu.com/server/docs/how-to/security/firewalls/>
- Docker packet filtering and firewalls: <https://docs.docker.com/engine/network/packet-filtering-firewalls/>
- NGINX documentation: <https://nginx.org/en/docs/>
