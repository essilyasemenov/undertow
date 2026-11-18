# Architecture: from diagnostics to acceptance

A reference for choosing and checking an access setup on Remnawave. Product facts rely on the official documentation (listed at the end). Claims without such backing are marked as engineering practice or observation.

## Contents

1. Diagnostics first
2. Topology options
3. Direct entry to a Node
4. Panel protection
5. Cascade through an intermediate VPS
6. Selective exit through WARP
7. Transparent proxying on a router
8. Entry through a CDN
9. Basic server security
10. Acceptance and failure analysis
11. Sources

## 1. Diagnostics first

Change the setup only after it is clear at which layer access breaks. The same "it doesn't work" symptom can come from very different causes.

| What is observed | Where to look | How to confirm |
| --- | --- | --- |
| The resource opens by IP but not by name | DNS resolution | compare the answer of the provider's DNS and an encrypted resolver (DoH/DoT) |
| The TCP connection is established, the TLS handshake breaks | SNI filtering or a certificate problem | `openssl s_client` with different `-servername` values |
| Small requests pass, long downloads freeze | rate limiting of long-lived connections, or MTU | the same address from another provider or VPS; an MTU check (skill `network`) |
| TCP works, UDP and QUIC do not | UDP filtering | the client in TCP-only mode |
| A foreign VPS is unreachable, a VPS in your own country is reachable | a policy by destination or address | a path through an intermediate VPS |
| The proxy works, but a particular site refuses | reputation or country of the exit IP | an exit for that site through another address (section 6) |
| Works from one device, not through the router | transparent proxying, a routing loop, DNS | check through SOCKS first (section 7) |

For each test, record the network and provider, location, time, protocol, destination and client version. Do not draw conclusions about the behavior of "the whole country" from one provider or one measurement.

## 2. Topology options

| Setup | When it fits | What it gives | What it costs |
| --- | --- | --- | --- |
| Client → foreign Node | the direct path is stable | the fewest components, the easiest to fix | all traffic depends on one foreign address being reachable |
| Client → intermediate VPS → foreign Node | the direct path degrades or is blocked | a different first hop, a fallback can be added | extra latency and one more server |
| Cascade + WARP exit for some sites | particular services reject the VPS address | compatibility with those services | one more dependency; only for selected domains |
| Router → cascade | many devices, or devices without a client | no client needed on every device | router resources, complex routing |
| Client → CDN → origin | the CDN edge is reachable, the direct address is not | a different entry into the network, TLS on a real domain | a domain, certificates, CDN transport limitations; Reality does not fit |

Start with the direct setup: it serves as a reference point even if something more complex is needed in the end. Add each next link only when diagnostics have shown why it is needed.

## 3. Direct entry to a Node

The base setup on Remnawave:

- a server with a supported Linux (the Remnawave docs recommend Ubuntu or Debian), with Remnawave Node installed per the official instructions; Xray-core runs inside the Node container;
- the inbound is described in a Config Profile on Panel; for a direct path, VLESS with `security: reality` is typical;
- port `443`, if it is free;
- for Reality, the inbound sets `target` (the address and port of a real TLS site; in old versions and guides the field was called `dest`, now both names are synonyms, use `target` in new configurations), `serverNames` (the names the server accepts; the Xray documentation advises taking them from the SAN of the `target` certificate), `privateKey` (the key pair is generated with `xray x25519`) and `shortIds`;
- outbounds `freedom` (direct exit) and `blackhole` (blocking).

The choice of transport on top of Reality (TCP with Vision, XHTTP and others) depends on server and client support; the Xray documentation describes the options but does not name one of them as best for all networks.

Checks on the Node (the `/opt/remnanode` directory comes from the official instructions; for a non-standard installation, see skill `remnawave`):

```bash
ss -lntup
cd /opt/remnanode && docker compose ps
docker compose logs --since 10m
docker exec remnanode xlogs
```

The Remnawave subscription gives clients the connection parameters (UUID, address, port, transport, key, SNI, short ID) from the Config Profile and Hosts data. The subscription link is a secret. Configuring Config Profiles, Hosts and Squads: skill `remnawave`.

## 4. Panel protection

Before the panel becomes reachable from outside:

- HTTPS only, through a reverse proxy; the Remnawave docs forbid publishing services directly;
- unique strong admin credentials; passkey or OAuth login, if configured;
- restrict access to the panel: a firewall by address, a private admin network, or Cloudflare Tunnel with Access (skill `cloudflare`), or the additional layers from the Panel Security section of the Remnawave docs;
- regular backups of the database and configuration.

Old installation scripts and UI field names from third-party articles may not match the current version; the reference point is the current documentation.

## 5. Cascade through an intermediate VPS

Three ways to link the intermediate server with the foreign one, from simple to complex.

### 5.1. Forwarding by the kernel (iptables)

Fits when one port of the intermediate server must be passed unchanged to one foreign address. Traffic is not decrypted, and the load is minimal.

Order:

1. Make sure there is backup access to the server besides SSH (the provider console).
2. Save the current rules: `iptables-save > /root/iptables.backup`.
3. Enable packet forwarding permanently (`net.ipv4.ip_forward = 1` in `/etc/sysctl.d/`).
4. Allow loopback, established connections, SSH and the forwarded port.
5. Add a DNAT rule in the `nat` table (`PREROUTING` chain) for the needed port to the foreign address; UDP only if the transport needs it.
6. Add `MASQUERADE` (`POSTROUTING` chain) and allow rules in `FORWARD` only for this direction.
7. Tighten the default policy last, and check access from a second SSH session without closing the first.
8. Save the rules so they survive a reboot, and verify this with a reboot.

Do not flush other people's rules on a production server wholesale; when replacing them, rely on the saved copy.

### 5.2. HAProxy in TCP mode

Fits when backend health checks, several foreign servers or load balancing are needed.

- `mode tcp` in `frontend` and `backend`: HAProxy forwards the stream without parsing TLS.
- Explicit `timeout connect`, `timeout client`, `timeout server`.
- The `check` parameter on backend servers enables health checks.
- Choose the `balance` algorithm for the load: `roundrobin`, `leastconn` for long connections, `source` to pin a client to a server.
- If a statistics page is needed, listen only on `127.0.0.1` or in the admin network.
- Without extra settings, the foreign Node sees the HAProxy address, not the client: IP limits and connection logs merge all users into one address. The HWID device limit does not depend on this: Remnawave counts devices by client headers when the subscription is requested, not by the connection address. To pass the real client address, enable PROXY protocol: in HAProxy, the `send-proxy-v2` parameter on the `server` line; on the Xray inbound in the Config Profile, `acceptProxyProtocol: true` in the transport settings. After that the inbound closes any connection without a PROXY header, so all clients of this inbound must come only through HAProxy.

Before applying:

```bash
haproxy -c -f /etc/haproxy/haproxy.cfg
systemctl reload haproxy
```

### 5.3. Intermediate Node with Xray

Fits when the intermediate server must decide where to send traffic itself: for example, Russian sites directly, everything else to the foreign Node. In Remnawave this is the server-side routing (bridge) setup from the docs; how to build it: skill `remnawave`.

What to keep in mind:

- clients and the "intermediate → foreign" link have different credentials;
- outbounds have clear unique tags (for example, `DIRECT`, `BLOCK`, the outbound to the foreign Node);
- Xray checks routing rules from top to bottom and applies the first match, so specific rules (`geosite:…`, `geoip:…`) go above the general rule to the foreign Node; traffic that matches no rule goes to the first outbound in the list;
- domain-based routing needs sniffing on the inbound (`destOverride`: `http`, `tls`, `quic`);
- each geosite and geoip category is a separate entry in the rule.

The cost: the intermediate server decrypts and re-encrypts traffic, which means CPU load, extra latency and one more place where the client's TLS fingerprint may differ from the expected one. If domain-based routing is not needed, options 5.1 and 5.2 are simpler.

## 6. Selective exit through WARP

If particular sites reject the address of the foreign VPS, traffic to only those sites can exit through Cloudflare WARP on the same server.

1. Install the client from the official Cloudflare package repository (`pkg.cloudflareclient.com`), package `cloudflare-warp`.
2. Register the client: `warp-cli registration new`.
3. Switch the client to local proxy mode (list of modes: `warp-cli mode --help`). In this mode the client listens for SOCKS on `127.0.0.1`, default port `40000`, and passes only traffic explicitly sent to the proxy.
4. Connect: `warp-cli connect`.
5. Check through the proxy: the response of `curl --socks5-hostname 127.0.0.1:40000 https://www.cloudflare.com/cdn-cgi/trace` must contain the line `warp=on`.
6. In the Config Profile, add a `socks` outbound to `127.0.0.1:40000` (Remnawave Node runs with `network_mode: host`, so the host address is reachable from the container) and a routing rule that sends only the needed domains to it.
7. Make sure all other traffic still goes through `freedom`.

The `warp-cli` syntax has changed between versions; if it differs, the current Cloudflare documentation is the source of truth. Do not send all traffic through WARP without an explicit task: it changes the exit address for all users of the Node.

## 7. Transparent proxying on a router

Needed when a client cannot be installed on every device. Step-by-step setup of specific firmware is outside this reference; below are the rules common to any implementation.

Exclude from transparent proxying:

- the address of the server the router itself connects to, otherwise the tunnel will loop into itself;
- local networks and the router's own addresses;
- loopback, multicast, broadcast and router management paths;
- any addresses needed to establish the tunnel (for example, DNS for resolving the server name).

Before enabling transparent mode, check the path through SOCKS:

```bash
curl https://ifconfig.me
curl --socks5-hostname 127.0.0.1:1080 https://ifconfig.me
```

The first address is the provider exit, the second is the exit through the proxy. Detection signals of a router-based setup: skill `detection-audit`.

## 8. Entry through a CDN

A CDN routes the connection by the real domain name and terminates TLS on its side. So only transports over HTTP(S) with a real domain pass through a CDN, and Reality, which needs its own handshake with the server, does not.

A typical path for Cloudflare:

```text
client or intermediate VPS
  -> CDN edge (TLS, port 443)
  -> nginx on the origin with a valid certificate
  -> 127.0.0.1 or Unix socket
  -> Xray: VLESS over WebSocket or gRPC, without its own TLS
```

Requirements:

- the domain is connected to the CDN, the DNS record is `Proxied`;
- a valid certificate on the origin, SSL/TLS mode `Full (strict)`;
- the needed features are enabled in the zone settings: WebSocket works on any HTTPS port from Cloudflare's list, gRPC only on `443`; Cloudflare does not confirm XHTTP specifically (skill `cloudflare`);
- nginx passes only the secret path to Xray and answers other requests with an ordinary site or a standard error;
- Xray listens on `127.0.0.1` or a Unix socket. In Remnawave, Xray runs inside the Node container with `network_mode: host`, so `127.0.0.1` is reachable by nginx on the host without extra settings; a Unix socket must be in a directory mounted into the Node container and accessible to nginx;
- the client uses `security=tls`, the real domain as SNI and Host, and the same path.

Check:

```bash
nginx -t
curl -I https://example.com/
openssl s_client -connect example.com:443 -servername example.com
```

If DNS allows it, check the direct path to the origin and the path through the CDN separately.

## 9. Basic server security

Engineering practice common to all setups:

- SSH with keys only; disable password and root login after backup access has been verified; keep a second session open while changing the firewall;
- keep the system updated, do not pin outdated package repositories;
- listen only on the needed addresses, open only the needed ports in the firewall;
- separate random credentials for each link of the chain and each client;
- reissue leaked UUIDs, keys, passwords, links and certificates;
- do not leave subscription links in logs, screenshots, tickets or shell history;
- read third-party installation scripts before running them, prefer pinned versions and checksum verification;
- store configuration backups with `0600` permissions;
- do not publish statistics, admin interfaces, SOCKS or DNS to the outside;
- take into account the provider's terms and local law.

## 10. Acceptance and failure analysis

### Layer-by-layer check

After each change, check in order:

1. The service starts without configuration errors.
2. The needed port listens on the needed address.
3. The client completes the transport and TLS/Reality handshake.
4. The external IP through the proxy matches the intended exit point.
5. The selected domains go through the intended outbound.
6. Other domains go directly where split routing is configured.
7. DNS resolves through the intended resolver and returns working A/AAAA records.
8. TCP and UDP behave as intended.
9. The setup survives a reboot.
10. Rollback restores the original access.

### Typical failures

| Failure | Where to start |
| --- | --- |
| The connection is refused immediately | whether the service listens, the firewall, the correct address and port |
| TLS error | SNI, certificate chain, server time, SSL/TLS mode in the CDN |
| The Reality handshake fails | `target` and `serverNames`, keys, short ID, the client's TLS fingerprint |
| Works through SOCKS, not transparently | nftables rules, packet marks, the routing table, loop exclusions |
| A domain rule does not match | sniffing, `domainStrategy`, rule order, geosite data |
| The CDN answers with an HTTP error | Host and path, WebSocket or gRPC headers, whether the origin listens |
| SSH is lost after a firewall change | rule order and the `INPUT` policy, the real SSH port, the provider console |
| High load or latency | double TLS termination, router capacity, choice of transport |
| Some apps bypass the policy | IPv6, QUIC/UDP, DNS built into the app, certificate pinning |

If changing the client's TLS fingerprint helps in observations, record it as an observation with the client version and date, not as a universal solution.

## 11. Sources

- Xray-core documentation: <https://xtls.github.io/config/> — routing, sniffing, outbounds, transports (including `acceptProxyProtocol`), REALITY.
- Remnawave documentation: <https://docs.rw/> — Node installation, Config Profiles, server-side routing, Panel Security.
- Cloudflare WARP for Linux: <https://developers.cloudflare.com/warp-client/get-started/linux/>; client modes, including local proxy: <https://developers.cloudflare.com/cloudflare-one/team-and-resources/devices/cloudflare-one-client/configure/modes/>.
- Network ports, WebSocket and gRPC through Cloudflare: <https://developers.cloudflare.com/fundamentals/reference/network-ports/>, <https://developers.cloudflare.com/network/websockets/>, <https://developers.cloudflare.com/network/grpc-connections/>.
- HAProxy: <https://docs.haproxy.org/>.
- nginx: <https://nginx.org/en/docs/>.
- netfilter/iptables: <https://www.netfilter.org/documentation/>.
