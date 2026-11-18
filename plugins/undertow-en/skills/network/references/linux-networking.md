# Linux Networking

## 1. What it is

`Linux networking` is the network model of a Linux host: interfaces, addresses, routes, sockets, listening services and diagnostics. For VPN infrastructure it is the base layer on which panels, reverse proxies, agents and auxiliary services run.

## 2. Why it is needed

- to understand on which address and port a service actually accepts traffic;
- to check addresses, routes and reachability on the server;
- to localize a problem: the application, the host network, the firewall or the upstream network;
- to publish services securely and restrict which addresses they listen on.

## 3. How it relates to VPN infrastructure

- almost all VPN panels and auxiliary services run on Linux hosts;
- without understanding interfaces, bind addresses, routes and sockets it is hard to diagnose `Remnawave`, `NGINX` or subscription pages;
- it is the foundation of the server side of VPN management.

## 4. How it relates to Cloudflare

- when publishing through Cloudflare, the origin is still a Linux host with its own interfaces, listening sockets and routes;
- the edge layer does not remove the need to understand the bind address, local reachability and the host firewall;
- diagnosing "Cloudflare does not work" often comes down to the state of the origin.

## 5. How it relates to Remnawave

- the `Remnawave` Panel, Node and subscription page run on Linux hosts in Docker; Panel listens on `127.0.0.1:3000`, Node runs with `network_mode: host`;
- `Nginx Proxy Manager` and plain `NGINX` depend on which address the upstream listens on and whether it is reachable.

## 6. Common mistakes

- looking only at the application and not checking the bind address;
- confusing `127.0.0.1`, `0.0.0.0`, a private network address and a public address;
- assuming a listening socket guarantees reachability from outside;
- changing routing or the firewall without checking the return path;
- looking for the problem in Cloudflare or the proxy when the process on the origin does not listen on the needed port.

## 7. Diagnostics

1. Check interface state, IP addresses and the routing table.
2. Check listening sockets and bind addresses.
3. Check reachability locally and from outside.
4. Check the chain `DNS -> TCP/UDP -> listening process`.
5. Distinguish an application problem, a host network problem, a firewall problem and an external edge problem.

```bash
ip -br addr
ip route
ss -lntup
```

## 8. Practical examples

- Diagnosing Remnawave Panel that listens only on `127.0.0.1`.
- Checking the `Remnawave` panel behind `NGINX` when the upstream is unreachable at the local address.
- Analyzing why the Cloudflare edge cannot connect to a Linux origin.
- Checking Remnawave Node (`Xray-core`) after changing interfaces or routing rules.

## 9. Checklist

- Check interface state, IP addresses and routes.
- Check which addresses the process listens on (`listen` / `bind`).
- Separate a host-side problem from an edge-side problem.
- Do not confuse local reachability with public reachability.
- If needed, go to `reverse-proxy.md`, `firewall.md` and `https.md`.

## Sources

- NGINX documentation: <https://nginx.org/en/docs/>
- Cloudflare Learning Center: <https://www.cloudflare.com/learning/>
